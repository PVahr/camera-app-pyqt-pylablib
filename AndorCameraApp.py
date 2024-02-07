import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QTime, QEvent
from PyQt5.QtGui import QPixmap, QImage
from pyqtgraph import PlotWidget
import time
import pylablib as pll
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from datetime import datetime
import re
from CameraApp_via_QT import Ui_CameraAppGUI

# !!! INSTALL LATEST PYQT using pip LIKE BELOW OTHERWISE THE qimage format grayscale 16 WILL NOT WORK!!!
pll.par["devices/dlls/andor_sdk2"] = "C:\Program Files\Andor Driver Pack 2"
from pylablib.devices import Andor

'''
Andor luca gives back 12 bit images!!!! Max value 4096
Two choices: convert everything to 8 bit grayscale images (easier but you loos 2**4, 16 times of color depth)
or convert to 16-bit Grayscale images, retaining the color depth (heavier and qimage gives problem in older versions
installed via conda)
'''


class CameraHandler:
    '''
    This class wraps the pylablib camera functions.
    You can change the wrapper to adapt it to your camera.

    - max_frame_size is set to 1000px*1000px (the default format is 1002*1004, super annoying to work with those
    2/4 pixels more)

    Functions           Bool
    open(), close()     is_opened()
    setup_acquisition, close_acquisition()      is_acquisition_setup()
    start/stop_acquistion()         acquisition_in_progess()

    '''
    def __init__(self, frame_period = 0.001, exposure_time=0.2, gain=2, stabilize_temp=False, binning=1):
        print('In __init__ of CameraHandler')
        self.cam = Andor.AndorSDK2Camera(idx=0, temperature=-20, fan_mode='full')
        self.open_camera()
        self.cam.set_frame_format('chunks')
        self.cam.set_frame_period(frame_period)
        self.cam.set_image_indexing('rct')
        self.exposure_time = exposure_time
        self.set_exposure_time(self.exposure_time)
        self.gain = gain
        self.set_gain(self.gain)

        if stabilize_temp:
            print('Temperature status', self.cam.get_temperature_status())  # you want to reach 'stabilized'
            start_cool_down_time = time.time()
            cool_down_time = 0
            temp_stabilized = False
            while not temp_stabilized and cool_down_time < 20:
                if self.cam.get_temperature_status() == 'stabilized':
                    temp_stabilized = True
                print('Temp status', self.cam.get_temperature_status(), ' at time ', cool_down_time)
                time.sleep(1)
                cool_down_time = time.time() - start_cool_down_time
            print('Time to stabilized temperature', cool_down_time)


        # frame dimension and roi size
        self.max_frame_size = [1000, 1000] # CHANGE HERE if camera is different
        self.roi_current_size = self.max_frame_size # init with biggest ROI possible
        self.roi_current_center = [int(self.max_frame_size[0]/2), int(self.max_frame_size[1]/2)] # center of the ROI, by default the center of the frame but can be changed in GUI
        self.roi_default_center = [int(self.max_frame_size[0]/2), int(self.max_frame_size[1]/2)] # default one
        print('Max frame size is ', self.cam.get_data_dimensions(), ' but will immediately set to max ', self.max_frame_size)
        self.set_ROI(self.max_frame_size, self.roi_default_center)

        self.frame = np.zeros(self.cam.get_data_dimensions(), dtype=np.uint16)  # init of camera frame
        self.binning = binning # default binning. Available are 2, 4, 8, 16. It can create a last line of dead pixel
        self.roi_size_1000, self.roi_size_512, self.roi_size_256, self.roi_size_128 = [1000, 1000], [512, 512], [256, 256], [128, 128] # neat ROIs

        print('max_frame_size, Default roi rize, default roi center, default binning: ', self.max_frame_size, self.roi_current_size, self.roi_current_center)
        print('Get device info', self.cam.device_info)

        self.setup_acquisition()
        self.timeout_on_camera = False

    def open_camera(self):
        if not self.cam.is_opened():
            self.cam.open()
            print('Camera now is open.')
            print('\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                  self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())

    def close_camera(self):
        print('Before closing camera.\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progress ',
              self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())
        if self.acquisition_in_progress():
            self.cam.stop_acquisition()
        if self.cam.is_acquisition_setup():
            self.cam.clear_acquisition()
        if self.cam.is_opened():
            self.cam.close()
        print('...closed.')
    def setup_acquisition(self):
        self.open_camera()
        if not self.cam.is_acquisition_setup():
            self.cam.setup_acquisition(mode='cont')  # mode = snap, kinetic, sequence, cont, nframes=100 is buffer size
            print('Acquisition params: ', self.cam.get_acquisition_mode(), self.cam.get_acquisition_parameters())
        else:
            print('Trying to setup acquisition, but it is already setup')
        print('In setup acquisition.\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
              self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())
        # print('Acquisition params: ', self.cam.get_acquisition_mode(), self.cam.get_acquisition_parameters())
        # default acquistion is continuos. Nframes not necessary with Andor, already fixed at around 100 frames

    def clear_acquisition(self):
        if self.acquisition_in_progress():
            self.stop_acquisition()
        if self.cam.is_acquisition_setup():
            self.cam.clear_acquisition()
            print('Aquisition Cleared')
        else:
            print('... in clear_acquisition but acquisition is not running!')
        print('\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                  self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())

    def start_acquisition(self):
        self.setup_acquisition()
        if not self.acquisition_in_progress():
            self.cam.start_acquisition()
            print('Started acquisition.\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                  self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())
        elif self.timeout_on_camera:
            print('Acquisition might be on but camera timeout, I try to restart acquisition anyway')
            self.cam.start_acquisition()
            self.timeout_on_camera = False
        else:
            print('Acquisition should be already on.\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                  self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())

    def stop_acquisition(self):
        if self.acquisition_in_progress():
            self.cam.stop_acquisition()
            print('Stopped acquisition.\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                  self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())
        else:
            print('Trying to stop acquisition, but is already stopped.)')
            print('\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                  self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())
    def set_exposure_time(self, exposure_time=None):
        if exposure_time==None: # I changed self.exposure_time from the GUI already
            exposure_time = self.exposure_time
            print('Exposure time from gui', self.exposure_time)
        self.cam.set_exposure(exposure_time)
        self.exposure_time = self.cam.get_exposure()
        print('Now self.exposure_time in CameraHandler is ', self.exposure_time, ' s')

    def set_gain(self, gain=None):
        if gain == None:
            gain = self.gain
            print('Updating gain from the GUI to ', self.gain)
        self.cam.set_EMCCD_gain(gain)
        self.gain = self.cam.get_EMCCD_gain()[0]
        print('Now self.gain in CameraHandler is ', self.gain)

    def set_ROI(self, roi_size, roi_center = None, binning=1):
    # self.cam.set_roi takes as arguments hstart, hend, vstart, vend, binning_x, binning_y
        print('in set_ROI, new roi size, new roi center', roi_size, roi_center)
        if not (roi_size[0] % 2 == 0):
            roi_size[0] = roi_size[0] + 1
            print('strecthed roi of one pixel horizontal to make it even, roi_size[0]', roi_size[0])
        if not (roi_size[1] % 2 == 0):
            roi_size[1] = roi_size[1] + 1
            print('strecthed roi of one pixel vertically to make it even. Will crash if alrady 1004, roi_size[1]', roi_size[1])
        if roi_center is not None:
            self.roi_current_center = roi_center
         # check if there is enough space, both when changing the center and when changing the ROI size
        if self.roi_current_center[0] - int(roi_size[0]*0.5) < 0:
            self.roi_current_center[0] = int(roi_size[0]*0.5)
            print('***** new roi center too much on the left, roi size roi center', roi_size, self.roi_current_center, '*****')
        if self.roi_current_center[0] + int(roi_size[0]*0.5) > self.max_frame_size[0]:
            self.roi_current_center[0] = self.max_frame_size[0] - int(roi_size[0]*0.5)
            print('***** new roi center too much on the right, roi size roi center', roi_size, self.roi_current_center, '*****')
        if self.roi_current_center[1] - int(roi_size[1]*0.5) < 0:
            self.roi_current_center[1] = int(roi_size[1]*0.5)
            print('***** new roi center too much on the bottom, roi size roi center', roi_size, self.roi_current_center, '*****')
        if self.roi_current_center[1] + int(roi_size[1]*0.5) > self.max_frame_size[1]:
            self.roi_current_center[1] = self.max_frame_size[1] - int(roi_size[1]*0.5)
            print('***** new roi center too much on the top, roi size roi center', roi_size, self.roi_current_center, '*****')
        self.roi_current_size = roi_size
        self.binning = binning
        hstart = self.roi_current_center[0] - int(self.roi_current_size[0]*0.5)
        hend = self.roi_current_center[0] + int(self.roi_current_size[0]*0.5)
        vstart = self.roi_current_center[1] - int(self.roi_current_size[1]*0.5)
        vend = self.roi_current_center[1] + int(self.roi_current_size[1]*0.5)
        if not isinstance(binning, int) or  not (binning in [1, 2, 4, 8, 16]):
            print('Invalid binning value, I set it to 1. Possible values are 1, 2, 4, 8, 16')
            binning = 1
        self.cam.set_roi(hstart, hend, vstart, vend, binning, binning)
        # print('camera dget dim', self.cam.get_data_dimensions())
        print('Exiting setRoi, roi_current_size ', self.roi_current_size, 'roi_center', self.roi_current_center)

    def set_binning(self, binning):
        if not isinstance(binning, int) or  not (binning in [1, 2, 4, 8, 16]):
            print('Invalid binning value, I set it to 1. Possible values are 1, 2, 4, 8, 16')
            binning = 1
        print('entering set_binning, self.roi_current_size, self.roi_current_center, self.binning', self.roi_current_size, self.roi_current_center, self.binning)
        self.binning = binning
        hstart = self.roi_current_center[0] - int(self.roi_current_size[0]*0.5)
        hend = self.roi_current_center[0] + int(self.roi_current_size[0]*0.5)
        vstart = self.roi_current_center[1] - int(self.roi_current_size[1]*0.5)
        vend = self.roi_current_center[1] + int(self.roi_current_size[1]*0.5)
        self.cam.set_roi(hstart, hend, vstart, vend, binning, binning)
        # print('cam.get_data_dimension()', self.cam.get_data_dimensions())
        print('exiting set_binning, self.roi_current_size, self.roi_current_center, self.binning', self.roi_current_size, self.roi_current_center, self.binning)



    def snap(self):
        if self.acquisition_in_progress():
            print(
                'Snapping while acquisition is livestreaming. I stop the stream, then take the snap, then turn on the stream again')
            self.stop_acquisition()
            frame = np.squeeze(self.cam.snap()).astype(np.uint16)
            self.start_acquisition()
            return frame
        else:
            if self.cam.is_acquisition_setup():
                print('Snap while not running!!')
                return np.squeeze(self.cam.snap())
            else:
                print('Trying to snap but acquisition not setup!')
                print('\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                      self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())

    def grab(self, num_frames, return_only_the_avg=True):
        if self.acquisition_in_progress():
            print('Grabbing while acquisition is livestreaming. I stop the stream, then grab ', num_frames,
                  ' num frames, then turn on the stream again')
            self.stop_acquisition()
            frame = np.squeeze(np.mean(self.cam.grab(nframes=num_frames)[:],
                                       axis=0))  # I swear it works :) I've checked with manual avgs
            frame = frame.astype(np.uint16)
            self.start_acquisition()
            return frame
        else:
            if self.cam.is_acquisition_setup():
                print('Grab while not running!!')
                return np.squeeze(np.mean(self.cam.grab(nframes=num_frames)[:], axis=0))
            else:
                print('Trying to grab but acquisition not setup!')
                print('\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                      self.cam.is_opened(), self.cam.is_acquisition_setup(), self.acquisition_in_progress())

    def wait_for_frame(self):
        if self.acquisition_in_progress():
            self.cam.wait_for_frame()
        else:
            print('In waiting for frame but we are not running')
            return None

    def read_oldest_image(self):
        if self.acquisition_in_progress():
            return self.cam.read_oldest_image()
        else:
            print('Trying read_oldest_image, but self.acquisition_in_progress() is False')

    def acquisition_in_progress(self):
        '''This replaces the self.acquisition_in_progress(), which can throw an error if
        called when cam.close() is already called'''
        try:
            status = self.cam.acquisition_in_progress()
            return status
        except Andor.base.AndorError:
            # print('Camera already closed')
            return False

'''
CameraThread to keep on reading the frames coming from the camera
it will stop reading frames when you change some settings (roi, binning, center, exposure time etc)
It will stop acquisition to snap or grab some frames
It will stop acqusition when dealing with opening and closing of the camera and killing itself

'''
class CameraThread(QThread):
    # these signal allow to call the methods that update the GUi in a thread safe way
    # ** UPDATING THE GUI FROM A NON-GUI THREAD IS NOT THREAD SAFE AND WILL LEAD TO CRASHES AND
    # swearing against a divinity of your choice
    processFrameSignal = pyqtSignal(np.ndarray)  # this sends for updating the whole frame
    saveFrameSignal = pyqtSignal(np.ndarray, bool, str, str)
    processGrabFrames = pyqtSignal(np.ndarray)  # use this signal to retrieve the frames in another app
    print('In CameraThread init')

    def __init__(self, window):
        super().__init__()
        self.window = window  # is this nasty? Probably
        self.isSnapButtonClicked = False  # Variable to keep track of button click
        self.isGrabButtonClicked = False  # Variable to keep track of button click
        self.isResetRoiButtonClicked = False
        self.isSetRoi512ButtonClicked = False
        self.isSetRoi256ButtonClicked = False
        self.isSetRoi128ButtonClicked = False
        self.isSetNewRoiCenterButtonClicked = False
        self.new_roi_center = self.window.camera.roi_current_center
        self.window.setCenterSignal.connect(self.handleNewROICenter)
        self.isResetRoiCenterButtonClicked = False
        self.isBinning1ButtonClicked = False
        self.isBinning2ButtonClicked = False
        self.isBinning4ButtonClicked = False
        self.isBinning8ButtonClicked = False
        self.isSetNewCameraSettingsClicked = False

        self.isStopAcquiButtonClicked = False
        self.isStartAcquiButtonClicked = False
        self.isClearAcquiButtonClicked = False
        self.isSetupAcquiButtonClicked = False
        self.isOpenCamButtonClicked = False
        self.isCloseCamButtonClicked = False
        self.isKillThreadButtonClicked = False
        self.save_while_running = False
        self.save_while_snap_or_grab = True
        self.nframes_to_grab = 10  # when pressing grab, will grab this much of frames and avg them into one
        print('***ACQUISITION FRAMERATE LIMITED BY USB BANDWIDTH/CAMERA READOUT TIME\n use BINNING and a SMALLER ROI to go down to 0.1 s!!!!\n(and enjoy life out of the lab too)***')

    def run(self):
        my_timeout = 60  # after this much, stop bothering the poor camera
        timer_100_frames = time.time()
        frame_counter = 0
        while True:
            frame = None
            if self.isSnapButtonClicked:
                print('In run of CameraThread, isSnapButtonClicked', self.isSnapButtonClicked)
                frame = self.window.camera.snap()
                timestamp = QTime.currentTime().toString("hh.mm.ss.zzz")
                if frame is not None:
                    self.processFrameSignal.emit(frame)
                    if self.save_while_snap_or_grab:
                        self.saveFrameSignal.emit(frame, False, 's',  timestamp)
                # time.sleep(
                #     self.window.camera.cam.get_exposure() * 3)  # wait 3 times the exposure time, then continue running
                self.isSnapButtonClicked = False
            if self.isGrabButtonClicked:
                print('In run of CameraThread, grabButtonClicked')
                frame = self.window.camera.grab(num_frames=self.nframes_to_grab, return_only_the_avg=True)
                timestamp = QTime.currentTime().toString("hh.mm.ss.zzz")
                if frame is not None:
                    self.processFrameSignal.emit(frame)
                    self.processGrabFrames.emit(frame)
                    if self.save_while_snap_or_grab:
                        self.saveFrameSignal.emit(frame, False, 'g', timestamp)
                self.isGrabButtonClicked = False
                # time.sleep(
                #     self.window.camera.cam.get_exposure() * self.nframes_to_grab)  # needed to display the longer avg
            if self.window.camera.acquisition_in_progress():
                try:
                    wait = time.time()
                    self.window.camera.cam.wait_for_frame(since='lastwait', timeout=60)
                    # 'lastread', 'lastwait', 'now', 'start'
                    # frame = np.squeeze(self.window.camera.cam.read_newest_image())
                    frame = np.squeeze(self.window.camera.cam.read_oldest_image())
                    timestamp = QTime.currentTime().toString("hh.mm.ss.zzz")
                    if np.any(frame == None):
                        continue
                    else:
                        frame_counter = frame_counter + 1
                    if frame_counter%100 == 0:
                        frame_counter = 0
                        print('Reading last frame took ', time.time() - wait, ' last 100 frames took', time.time() - timer_100_frames)
                        timer_100_frames = time.time()
                    self.processFrameSignal.emit(frame)
                    # self.processFrame_to_GUI(frame)  # Use the actual camera function
                    ######self.frameSignal.emit(frame)
                    # process_timestamp = time.time()
                    # print('Time (s) to processFrame_to_GUI(frame) ', process_timestamp - acqui_timestamp, timestamp)
                    if self.save_while_running:
                        self.saveFrameSignal.emit(frame, True, 'r' + str(self.window.processingThread.make_n_avg_then_save), timestamp)
                        # save_timestamp = time.time()
                        # print('If save while running, time to save ', save_timestamp - process_timestamp)
                    # exit_timestamp = time.time()
                except Andor.base.AndorTimeoutError:  # after 15 s on wait_for_frame() will throw errors
                    self.window.camera.timeout_on_camera = True
                    self.window.camera.stop_acquisition()
                    print(f'Timeout on camera')
                    continue  # this continue is detrimental to keep the cycle going on!
                except Andor.base.AndorError:
                    self.window.camera.stop_acquisition()
                    print(f'Camera not open?')
                    continue
            # stop acqui, reset ROI/binning, start acqui
            if self.isResetRoiButtonClicked or self.isSetRoi512ButtonClicked or self.isSetRoi256ButtonClicked or self.isSetRoi128ButtonClicked or self.isSetNewRoiCenterButtonClicked or self.isResetRoiCenterButtonClicked or self.isBinning1ButtonClicked or self.isBinning2ButtonClicked or self.isBinning4ButtonClicked or self.isSetNewCameraSettingsClicked or self.isBinning8ButtonClicked:
                print('In run of CameraThread, resize the ROI case/change center/change camera setting/etc')
                restart_acqui_after_change_in_ROI = False # remember to restart acqui if it was running
                if self.window.camera.acquisition_in_progress():
                    restart_acqui_after_change_in_ROI = True
                    self.window.camera.stop_acquisition()
                self.window.processingThread.center_line_from_mouse_horiz = None # wipe them to avoid IndexErrors when changing ROI
                self.window.processingThread.center_line_from_mouse_vert = None
                if self.isResetRoiButtonClicked:
                    self.window.camera.set_ROI(self.window.camera.roi_size_1000, roi_center=self.window.camera.roi_default_center, binning=self.window.camera.binning)
                    self.isResetRoiButtonClicked = False
                if self.isSetRoi512ButtonClicked:
                    self.window.camera.set_ROI(self.window.camera.roi_size_512, binning=self.window.camera.binning)
                    self.isSetRoi512ButtonClicked = False
                if self.isSetRoi256ButtonClicked:
                    self.window.camera.set_ROI(self.window.camera.roi_size_256, binning=self.window.camera.binning)
                    self.isSetRoi256ButtonClicked = False
                if self.isSetRoi128ButtonClicked:
                    self.window.camera.set_ROI(self.window.camera.roi_size_128, binning=self.window.camera.binning)
                    self.isSetRoi128ButtonClicked = False
                if self.isSetNewRoiCenterButtonClicked:
                    self.window.camera.set_ROI(self.window.camera.roi_current_size, roi_center=self.new_roi_center)
                    self.isSetNewRoiCenterButtonClicked = False
                if self.isResetRoiCenterButtonClicked:
                    self.window.camera.set_ROI(self.window.camera.roi_current_size, roi_center=self.window.camera.roi_default_center)
                    self.isResetRoiCenterButtonClicked = False
                if self.isBinning1ButtonClicked:
                    self.window.camera.set_binning(1)
                    self.isBinning1ButtonClicked = False
                if self.isBinning2ButtonClicked:
                    self.window.camera.set_binning(2)
                    self.isBinning2ButtonClicked = False
                if self.isBinning4ButtonClicked:
                    self.window.camera.set_binning(4)
                    self.isBinning4ButtonClicked = False
                if self.isBinning8ButtonClicked:
                    self.window.camera.set_binning(8)
                    self.isBinning8ButtonClicked = False
                if self.isSetNewCameraSettingsClicked:
                    self.window.camera.set_exposure_time()
                    self.window.camera.set_gain()
                    self.isSetNewCameraSettingsClicked = False
                if restart_acqui_after_change_in_ROI:
                    self.window.camera.start_acquisition()
            if self.isStopAcquiButtonClicked or self.isStartAcquiButtonClicked or self.isClearAcquiButtonClicked or self.isSetupAcquiButtonClicked or self.isOpenCamButtonClicked or self.isCloseCamButtonClicked:
                if self.isStopAcquiButtonClicked:
                    self.window.camera.stop_acquisition()
                    self.isStopAcquiButtonClicked = False
                if self.isStartAcquiButtonClicked:
                    self.window.camera.start_acquisition()
                    self.isStartAcquiButtonClicked = False
                if self.isClearAcquiButtonClicked:
                    self.window.camera.clear_acquisition()
                    self.isClearAcquiButtonClicked = False
                if self.isSetupAcquiButtonClicked:
                    self.window.camera.setup_acquisition()
                    self.isSetupAcquiButtonClicked = False
                if self.isOpenCamButtonClicked:
                    self.window.camera.open_camera()
                    self.isOpenCamButtonClicked = False
                if self.isCloseCamButtonClicked:
                    self.window.camera.close_camera()
                    self.isCloseCamButtonClicked = False
                print('After changing camera status\nCamera is_opened(), is_acquisition_setup(), acquisition_in_progss ',
                      self.window.camera.cam.is_opened(), self.window.camera.cam.is_acquisition_setup(), self.window.camera.acquisition_in_progress())

            if not self.window.camera.acquisition_in_progress():
                time.sleep(self.window.camera.exposure_time) # cause otherwise you spin at a crazy aZZ speed inside this loop!
            if self.isKillThreadButtonClicked:
                print('In run of CameraThread, isKillThreadButtonClicked True')
                break
        self.isKillThreadButtonClicked = False
        print('***** in Run of CameraThread, but OUTSIDE THE WHILE LOOP')
        # self.terminate()

    def handleNewROICenter(self,roi_x_center, roi_y_center):
        print('*** in handleNewROICenter of CameraThread*** ')
        self.isSetNewRoiCenterButtonClicked = True
        self.new_roi_center = [ int(roi_x_center), int(roi_y_center)]

class ProcessingThread(QThread):
    frameSignalToGui = pyqtSignal(np.ndarray)  # this sends for updating the whole frame
    horizontalSignal = pyqtSignal(np.ndarray)  # this the 1d array for the lower plot
    verticalSignal = pyqtSignal(np.ndarray)
    avgSignal = pyqtSignal(float)  # this the scalar containing the avg

    def __init__(self, window, directory_to_save_images):
        print('In ProcessingThread init')
        super().__init__()
        self.window = window  # is this nasty? Probably

        self.extensions = ['png'] # save pngs by default self.extensions = ['npy', 'png', 'tiff']
        self.save_also_raw_frame = False # or else, save also raw frame
        self.make_n_avg_then_save = 50 # will sum up N frames, then avg, then save them as one single frame
        self.make_n_avg_then_save_counter = 0 # this will count how many frames have been summed up
        self.frames_to_be_saved = np.zeros(self.window.camera.roi_current_size, dtype=np.float64) # use this to accumulate the frames to be saved
        self.frames_to_be_saved_raw = np.zeros(self.window.camera.roi_current_size, dtype=np.float64) # use this to accumulate the frames to be saved
        [self.save_img_dir, self.date_directory] = self.setupDirectoryToSaveFrame(directory_to_save_images)
        self.save_while_running = False
        self.save_while_snap_or_grab = True

        # setting for livestream of frames
        self.rescale_frame_automatically = True  # if False, use rescaling by user in GUI. Else, rescale every frame s.t. min is 0 max is 65635 (16 bit depth)
        self.rescale_frame_min = 0
        self.rescale_frame_max = 3000
        self.subtract_background = False
        self.background_frame = np.zeros(self.window.camera.roi_current_size, dtype=np.uint16)
        self.background_frame = np.random.randint(0, 65536, size=self.window.camera.max_frame_size, dtype=np.uint16)
        self.center_line_from_mouse_horiz = None  # this keeps the coordinates of a line set to the max value you can turn on with the mouse
        self.center_line_from_mouse_vert = None
        self.add_center_line_to_frames = False
        self.add_cursor_xy = False
        self.cursor_x_pixels = 20
        self.cursor_y_pixels = 20
    def run(self):
        while True:  # is this intelligent? Prob no, but neither am I
            time.sleep(0.001)
            # if cycle_counter%100 == 0:
            #     print('Running on Processing Thread with a time.sleep of 20 ms , cycle number ', cycle_counter)

    def processFrame_to_GUI(self, frame):
        '''
        For every frame acquired, this function does all the math and sends ONLY the final results, one at the time,
        to the GUI.
        Doing the math (like avg, integral, saving the frames) in the GUI thread is highly forbidden, as
        it leads to freezing and crashing.
        The QWidgets cannot be called from within this thread, so once all the math is done, the processed result
         is send only for the plotting bit to the GUI.
         This is a thread safe implementation
         This is also the place where to manipulate the thread further and send it to a saving function/thread, etc.
        '''
        if not np.any(frame == None):
            if self.window.verbose:
                print('Frame min, max, ptp, mean, type(frame), frame.shape', np.min(frame), np.max(frame), np.ptp(frame), np.mean(frame), frame.dtype,
                      type(frame), frame.shape)
            if self.rescale_frame_automatically:
                rescaled_frame = ((frame - np.min(frame)) * 65536 / np.ptp(frame)).astype(
                    np.uint16)  # conversion to Grayscale 16 bit + rescaling from 0 to 65536
            else:
                rescaled_frame = ((frame - self.rescale_frame_min) * 65536 / (
                            self.rescale_frame_max - self.rescale_frame_min)).astype(
                    np.uint16)  # conversion to Grayscale 16 bit + rescaling from 0 to 65536
            if self.window.verbose:
                print('Frame min, ptp, mean, frame.shape', np.min(rescaled_frame), np.ptp(rescaled_frame), np.mean(rescaled_frame), frame.dtype)

            if self.subtract_background:
                try:
                    rescaled_frame = rescaled_frame - self.background_frame
                except ValueError:
                    print('ValueError when substracting background frame. Check if size of frames is the same!')

            if self.add_center_line_to_frames and self.center_line_from_mouse_vert is not None and self.center_line_from_mouse_horiz is not None:
                if self.rescale_frame_automatically:
                    max = np.max(rescaled_frame)
                else:
                    max = self.rescale_frame_max
                if self.window.camera.roi_current_size[0]/self.window.camera.binning > 400: # this add a cross of 1 or 3 pixel (1 pixel too little at full res)
                    rescaled_frame[:, self.center_line_from_mouse_horiz-1:self.center_line_from_mouse_horiz+1] = max
                    rescaled_frame[self.center_line_from_mouse_vert-1:self.center_line_from_mouse_vert+1, :]  = max
                else:
                    rescaled_frame[:, self.center_line_from_mouse_horiz] = max
                    rescaled_frame[self.center_line_from_mouse_vert, :] = max
                if self.add_cursor_xy:
                    try:
                        cursor_x = int(self.cursor_x_pixels/self.window.camera.binning) # to compensate for the binning
                        cursor_y = int(self.cursor_y_pixels / self.window.camera.binning)  # to compensate for the binning
                        rescaled_frame[::3, self.center_line_from_mouse_horiz+cursor_x] = max
                        rescaled_frame[::4, self.center_line_from_mouse_horiz-cursor_x] = max
                        rescaled_frame[self.center_line_from_mouse_vert+cursor_y, ::3] = max
                        rescaled_frame[self.center_line_from_mouse_vert-cursor_y, ::3] = max
                    except IndexError:
                        print('X or Y cursors are outside the frame range, please resize them to be smaller')

            self.frameSignalToGui.emit(rescaled_frame)
            # compute integrals and send them to their plotting functions in the GUI thread
            integral_horizontal = np.mean(frame, axis=0)  # plot at the bottom
            self.horizontalSignal.emit(integral_horizontal)
            integral_vertical = np.mean(frame, axis=1)  # for plot on the right
            self.verticalSignal.emit(integral_vertical)

            self.avgSignal.emit(np.mean(frame))
            # print('Elapsed time for plotting ', time.time() - start_time)

        else:
            print('Passed a None frame to updateFrame')


    def saveFrame(self, frame, avg_frame, mode_to_append, timestamp):
        # avg_frames will sum up a number of frames equal to self.make_n_avg_then_save
        # storing them into self.frames_to_be_saved and saving a total of self.make_n_avg_then_save_counter
        # mode_to_append: a string that will be appended after im:
            # s = snap
            # g = gran
            # r = running
        # followed by the make_n_avg_then_save variable
        # timestamp a string formatted like HH:MM:SS.MMS hour minute second millisecond via QTime
        if not np.any(frame == None):
            if not os.path.exists(self.date_directory):
                print('The path to save images DOES NOT EXISTS. I refuse to save image. ', self.date_directory)
                return 1
            if self.rescale_frame_automatically: # first rescale the frame
                rescaled_frame = ((frame - np.min(frame)) * 65536 / np.ptp(frame)).astype(
                    np.uint16)  # conversion to Grayscale 16 bit + rescaling from 0 to 65536
            else:
                rescaled_frame = ((frame - self.rescale_frame_min) * 65536 / (
                        self.rescale_frame_max - self.rescale_frame_min)).astype(
                    np.uint16)  # conversion to Grayscale 16 bit + rescaling from 0 to 65536
            if avg_frame:
                try:
                    self.frames_to_be_saved = self.frames_to_be_saved + rescaled_frame
                    self.frames_to_be_saved_raw = self.frames_to_be_saved_raw + frame
                    self.make_n_avg_then_save_counter = self.make_n_avg_then_save_counter + 1
                    if self.make_n_avg_then_save_counter >= self.make_n_avg_then_save:
                        self.make_n_avg_then_save_counter = 0 # restart counting frames
                        frame = (self.frames_to_be_saved_raw/self.make_n_avg_then_save).astype(np.uint16)
                        rescaled_frame = (self.frames_to_be_saved / self.make_n_avg_then_save).astype(np.uint16)
                        print('Summed up ', self.make_n_avg_then_save, ' frames')
                        self.frames_to_be_saved = np.zeros(self.window.camera.roi_current_size, # empty the frames keeping the avg
                                                           dtype=np.float64)  # use this to accumulate the frames to be saved
                        self.frames_to_be_saved_raw = np.zeros(self.window.camera.roi_current_size,
                                                               dtype=np.float64)  # use this to accumulate the frames to be saved
                        avg_frame = False
                except ValueError:
                    # this case will always be triggered when you chnge roi size
                    # if so, re initialize the frames to be saved and set counter to 0
                    roi_size_w_binning = [int(self.window.camera.roi_current_size[0]/self.window.camera.binning), int(self.window.camera.roi_current_size[1]/self.window.camera.binning)]
                    self.frames_to_be_saved = np.zeros(roi_size_w_binning, dtype=np.float64)
                    self.frames_to_be_saved_raw = np.zeros(roi_size_w_binning, dtype=np.float64)
                    self.make_n_avg_then_save_counter = 0
                    print('ValueError on accumulating frames to be saved. I reinitialize them to the correct, new ROI size')

            if not avg_frame and self.extensions:
                for extension in self.extensions:
                    latest_file_info = self.find_latest_file_with_extension(self.date_directory, extension)
                    if latest_file_info is not None:
                        latest_file, latest_number = latest_file_info
                        next_number = latest_number + 1
                    else:
                        # If no files found, start from 0
                        next_number = 0
                    # Construct the filename with the progressive integer
                    # CHANGE HERE to append/change different params to the filename of every image
                    # im_ mode_to_append can be s (snap), g (grab), r (run)
                    # _exp0.5 # exposure time rounded to tens of ms
                    # _gain2 # EMCCD gain as integer
                    extra_info = 'exp' + str(np.round(self.window.camera.exposure_time, decimals=2)) + '_gain' + str(int(self.window.camera.gain))
                    base_filename = f"{datetime.now().strftime('%Y_%m_%d')}_{next_number:05d}_{timestamp}_im_{mode_to_append}_{extra_info}"
                    full_file_path = os.path.join(self.date_directory, f"{base_filename}.{extension}")
                    full_file_path_raw = os.path.join(self.date_directory, f"raw_{base_filename}.{extension}")
                    if extension == 'npy':
                        np.save(full_file_path, rescaled_frame)
                        print('Saved .' + extension + ' in ' + base_filename)
                        if self.save_also_raw_frame:
                            np.save(full_file_path_raw, frame)
                            print('Saved .' + extension + ' in raw_' + base_filename)
                    elif extension in ['png', 'tiff']:
                        pil_image = Image.fromarray(rescaled_frame)
                        pil_image.save(full_file_path)
                        print('Saved .' + extension + ' in ' + base_filename)
                        if self.save_also_raw_frame:
                            pil_image = Image.fromarray(frame)
                            pil_image.save(full_file_path_raw)
                            print('Saved .' + extension + ' in raw_' + base_filename)


    def setupDirectoryToSaveFrame(self, directory='./img'):
        save_img_dir = os.path.abspath(directory)
        if not os.path.exists(save_img_dir):
            os.makedirs(save_img_dir)
            print(f"Created main directory: {save_img_dir}")
        else:
            print('Found save_img_dir ', save_img_dir)
        current_date_str = datetime.now().strftime("%Y_%m_%d")
        date_directory = os.path.join(save_img_dir, current_date_str)
        if not os.path.exists(date_directory):
            os.makedirs(date_directory)
            print(f"Created date-specific directory: {date_directory}")
        else:
            print('Found date_directory ', date_directory)
        return save_img_dir, date_directory

    def find_latest_file_with_extension(self, directory, extension):
        # Get a list of files with the specified extension in the directory
        files = [file for file in os.listdir(directory) if file.endswith(f".{extension}")]

        # If no files are found, return None
        if not files:
            print('**** No files found with extensions ', extension, ' in folder ', directory)
            return None

        # Extract the progressive integer part from the filenames
        # CHANGE HERE if you change the filename structure (this function will most likely fail)
        pattern = re.compile(r"\d\d\d\d_\d\d_\d\d_(\d\d\d\d\d)_\d\d\.\d\d\.\d\d\.\d\d\d_im(_[\w\d\.\+\-]+)?\.(png|tiff|npy)")
        numbers = [int(pattern.search(file).group(1)) for file in files if pattern.search(file)]
        # If no integers are found in the filenames, return None
        if not numbers:
            print('**** No number found with extensions ', extension, ' in folder ', directory)
            return None

        # Return the latest filename and its corresponding progressive integer
        latest_file = files[numbers.index(max(numbers))]
        latest_number = max(numbers)
        return latest_file, latest_number


class CameraApp(QMainWindow, Ui_CameraAppGUI):
    setCenterSignal = pyqtSignal(int, int)
    def __init__(self, verbose=False, dummy_camera=False, dark_theme=False, directory_to_save_images=r'./img'):
        super(self.__class__, self).__init__()
        self.verbose = verbose
        self.dummy_camera = dummy_camera
        self.directory_to_save_images = directory_to_save_images
        if dark_theme:
            try:
                import qdarktheme
            except ModuleNotFoundError:
                print('Dark theme module not found. Install qdarktheme')
            qdarktheme.setup_theme()
            qdarktheme.enable_hi_dpi()

        self.setupUi(self)
        print('*** CameraApp GUI set up')
        self.initVariables()
        self.connectUi() # makes all the connections between the GUI and the functions

    def initVariables(self):
        # this only init variables and not GUI
        if self.dummy_camera:  # to run this code without a camera on the pc
            self.camera = DummyCameraHandler()
        else:
            self.camera = CameraHandler()  # this will keep a CameraHandler object

        self.thread = QThread()  # following https://realpython.com/python-pyqt-qthread/
        self.cameraWorkerThread = CameraThread(self)
        self.cameraWorkerThread.moveToThread(self.thread)
        # # connects the two threads
        self.thread.started.connect(self.cameraWorkerThread.run)
        self.thread.start()  # this will call the run method of the CameraThread

        self.processingThread = ProcessingThread(self, directory_to_save_images=self.directory_to_save_images)
        self.processingThread.start()
        self.cameraWorkerThread.saveFrameSignal.connect(self.processingThread.saveFrame)
        self.cameraWorkerThread.processFrameSignal.connect(self.processingThread.processFrame_to_GUI)
        self.processingThread.frameSignalToGui.connect(self.updateFrameOnGui)
        self.processingThread.horizontalSignal.connect(self.updateIntegralBottom)
        self.processingThread.verticalSignal.connect(self.updateIntegralRight)
        self.processingThread.avgSignal.connect(self.updateAvg)

        # self.aboutToQuit(self.onCloseCamButton)
        self.mean_plot_vector_length = 100
        self.mean_plot_vector = np.zeros(self.mean_plot_vector_length, dtype=np.float64)  # this keeps the avgs values to be plotted

        print('Exiting init variables of CameraApp')

    def connectUi(self):
        # ONLY gui STUFF
        print('Entering init of connectUI, be patient')

        # GUI stuff
        self.updateFrameOnGui(np.random.randint(0, 65536, size=self.camera.max_frame_size, dtype=np.uint16))
        self.canvas.setMouseTracking(True)
        self.canvas.installEventFilter(self)

        # PyqtPlotWidgets for plot at the bottom and right of the frame, and plot of the avg
        self.plot_bottom.setLabel('left', 'Intensity')
        self.plot_bottom.hideAxis("bottom")
        self.plot_right.setLabel('bottom', 'intensity')
        self.plot_right.hideAxis("left")
        self.plot_avg.showGrid(x=False, y=True)
        self.plot_avg.setLabel('left', 'avg intensity')

        # open close camera etc
        self.startAcqui.clicked.connect(self.onStartAcquiButton)
        self.stopAcqui.clicked.connect(self.onStopAcquiButton)
        self.clearAcqui.clicked.connect(self.onClearAcquiButton)
        self.setupAcqui.clicked.connect(self.onSetupAcquiButton)
        self.openCam.clicked.connect(self.onOpenCamButton)
        self.closeCam.clicked.connect(self.onCloseCamButton)
        self.snapButton.clicked.connect(self.onSnapButtonClicked)
        self.grabButton.clicked.connect(self.onGrabButtonClicked)
        self.clearPlotButton.clicked.connect(self.onClearPlotButtonClicked)
        self.restartCameraThreadButton.clicked.connect(self.onRestartCameraThreadButton)

        # to ROI settings layout
        self.resetRoiButton.clicked.connect(self.onResetRoiButton)
        self.setRoi512Button.clicked.connect(self.onSetRoi512Button)
        self.setRoi256Button.clicked.connect(self.onSetRoi256Button)
        self.setRoi128Button.clicked.connect(self.onSetRoi128Button)
        self.roiCenterXEdit.setText(str(self.camera.roi_default_center[0]))
        self.roiCenterYEdit.setText(str(self.camera.roi_default_center[1]))
        self.setNewRoiCenterButton.clicked.connect(self.onSetNewRoiCenterButton)
        self.resetRoiCenterButton.clicked.connect(self.onResetRoiCenterButton)
        self.binning1Button.clicked.connect(self.onbinning1Button)
        self.binning2Button.clicked.connect(self.onbinning2Button)
        self.binning4Button.clicked.connect(self.onbinning4Button)
        self.binning8Button.clicked.connect(self.onbinning8Button)
        self.automaticFrameScalingCheckbox.stateChanged.connect(self.onAutomaticFrameScalingCheckbox)
        self.frameMinEdit.setText(str(self.processingThread.rescale_frame_min))
        self.frameMaxEdit.setText(str(self.processingThread.rescale_frame_max))
        self.setFrameMinMax.clicked.connect(self.onsetFrameMinMax)
        self.frameMinEdit.returnPressed.connect(self.onsetFrameMin)
        self.frameMaxEdit.returnPressed.connect(self.onsetFrameMax)
        self.roiCenterXEdit.returnPressed.connect(self.onSetNewRoiCenterButton)
        self.roiCenterYEdit.returnPressed.connect(self.onSetNewRoiCenterButton)
        self.automaticFrameScalingCheckbox.setChecked(True)
        self.binning1Button.setStyleSheet('background-color: green;')
        self.resetRoiButton.setStyleSheet('background-color: green;')

        # to camera settings layout
        self.setNewCameraSettings.clicked.connect(self.onSetNewCameraSettings)
        self.setGainEdit.setText(str(self.camera.gain))
        self.setExposureEdit.setText(str(np.round(self.camera.exposure_time, decimals=3)))
        self.setNFramesToGrab.setText(str(self.cameraWorkerThread.nframes_to_grab))
        self.subtractBackgroundCheckbox.stateChanged.connect(self.onSubtractBackgroundCheckbox)
        self.selectBackgroundFileButton.clicked.connect(self.onSelectBackgroundFileButton)
        self.addMouseLineButton.clicked.connect(self.onAddMouseLineButton)
        self.addCursorsButton.clicked.connect(self.onAddCursorsButton)
        self.CursorHoriz.setText(str(self.processingThread.cursor_x_pixels))
        self.CursorVert.setText(str(self.processingThread.cursor_y_pixels))
        self.CursorHoriz.returnPressed.connect(self.onCursorHorizVert)
        self.CursorVert.returnPressed.connect(self.onCursorHorizVert)

        # to saving settings layout
        self.saveWhileSnapOrGrabCheckbox.setChecked(True) # start while saving by default while snap or grab
        self.savePngExtension.setChecked(True)
        self.setMakeNAvgThenSave.setText(str(self.processingThread.make_n_avg_then_save))
        self.saveWhileRunningCheckbox.stateChanged.connect(self.onSaveWhileRunningCheckbox)
        self.saveWhileSnapOrGrabCheckbox.stateChanged.connect(self.onSaveWhileSnapOrGrabCheckbox)
        self.saveAlsoRawFrame.stateChanged.connect(self.onSaveAlsoRawFrameCheckbox)
        self.saveNpyExtension.stateChanged.connect(self.onSaveNpyExtensionCheckbox)
        self.savePngExtension.stateChanged.connect(self.onSavePngExtensionCheckbox)
        self.saveTiffExtension.stateChanged.connect(self.onSaveTiffExtensionCheckbox)
        self.SetupSaveDirectory.clicked.connect(self.onSetupSaveDirectory)
        self.setMakeNAvgThenSave.returnPressed.connect(self.onSetMakeNAvgThenSave)
        self.dontPanickButton.clicked.connect(self.onDontPanickButton)

    @pyqtSlot(np.ndarray)
    def updateFrameOnGui(self, frame):
        # conversion to Grayscale 8 bit (loosing 2**4 = 16 factor in res :( )
        # frame =( frame/16 ).astype(np.uint8)
        # if Grayscale not found, u can switch to Format_Grayscale8. If so, change 65536 with 256 above.
        # QImage.Format_Grayscale16 requires pyqt5 > 5.12 or else will fail; install most recent with pip, not with conda
        qimg = QImage(frame.data, frame.shape[1], frame.shape[0],
                      QImage.Format_Grayscale16)
        pixmap = QPixmap.fromImage(qimg)
        # self.window.canvas.clear()  # Clear the existing pixmap, probably not needed
        self.canvas.setPixmap(pixmap.scaled(self.canvas.width(), self.canvas.height(), Qt.KeepAspectRatio))

    @pyqtSlot(np.ndarray)
    def updateIntegralBottom(self, integral_horizontal):
        self.plot_bottom.clear()
        self.plot_bottom.plot(integral_horizontal, fillLevel=np.min(integral_horizontal), brush=(50, 50, 200, 100))

    @pyqtSlot(np.ndarray)
    def updateIntegralRight(self, integral_vertical):
        self.plot_right.clear()
        self.plot_right.plot(integral_vertical[::-1], np.arange(len(integral_vertical))) # [::-1] flips the direction, or else it's flipped!

    @pyqtSlot(float)
    def updateAvg(self, frame_avg):
        if np.argmin(self.mean_plot_vector != 0) == 0 and np.count_nonzero(self.mean_plot_vector) >=self.mean_plot_vector_length:
            # then you've flled up the whole array, wipe it!
            self.mean_plot_vector = np.zeros(self.mean_plot_vector_length, dtype=np.float64)
        self.mean_plot_vector[np.argmin(self.mean_plot_vector != 0)] = frame_avg # add latest value to mean value vector
        self.plot_avg.clear()
        self.plot_avg.plot(self.mean_plot_vector[self.mean_plot_vector!=0])

    def onStopAcquiButton(self):
        self.cameraWorkerThread.isStopAcquiButtonClicked = True

    def onStartAcquiButton(self):
        self.cameraWorkerThread.isStartAcquiButtonClicked = True
    def onClearAcquiButton(self):
        self.cameraWorkerThread.isClearAcquiButtonClicked = True
    def onSetupAcquiButton(self):
        self.cameraWorkerThread.isSetupAcquiButtonClicked = True

    def onOpenCamButton(self):
        self.cameraWorkerThread.isOpenCamButtonClicked = True

    def onCloseCamButton(self):
        # self.cameraWorkerThread.isCloseCamButtonClicked = True
        self.cameraWorkerThread.isKillThreadButtonClicked = True
        time.sleep(1)
        self.cameraWorkerThread.terminate()

    def onRestartCameraThreadButton(self):
        print('Does not work')
        # self.cameraWorkerThread = CameraThread(self)
        # self.cameraWorkerThread.moveToThread(self.thread)
        # # # connects the two threads
        # self.thread.started.connect(self.cameraWorkerThread.run)
        # self.thread.start()  # this will call the run method of the CameraThread
        # self.cameraWorkerThread.run()
    # def onKillCameraThreadButton(self):
    #     print('Trying to kill cameraThread')
    #     # self.cameraWorkerThread.finished.disconnect(self.handleThreadFinished)
    #     if self.thread.isRunning():
    #         self.thread.quit()
    #         self.thread.wait()
    #     print('Killed?')
    # def onRestartCameraThreadButton(self):
    #     print('Trying to restart amera thread')
    #     if not self.thread.isRunning():
    #         print('Thread not running')
    #         # self.cameraWorkerThread.finished.connect(self.handleThreadFinished)
    #         self.thread.start()
    #     else:
    #         print('self.thread.isRunning  is True')
    def onSnapButtonClicked(self):
        self.cameraWorkerThread.isSnapButtonClicked = True

    def onGrabButtonClicked(self):
        self.cameraWorkerThread.isGrabButtonClicked = True

    def onClearPlotButtonClicked(self):
        self.mean_plot_vector = np.zeros(self.mean_plot_vector_length, dtype=np.float64)
        self.plot_avg.clear()

    def onResetRoiButton(self):
        self.cameraWorkerThread.isResetRoiButtonClicked = True
        self.resetRoiButton.setStyleSheet('background-color: green;')
        self.setRoi512Button.setStyleSheet('')
        self.setRoi256Button.setStyleSheet('')
        self.setRoi128Button.setStyleSheet('')

    def onSetRoi512Button(self):
        self.cameraWorkerThread.isSetRoi512ButtonClicked = True
        self.resetRoiButton.setStyleSheet('')
        self.setRoi512Button.setStyleSheet('background-color: green;')
        self.setRoi256Button.setStyleSheet('')
        self.setRoi128Button.setStyleSheet('')

    def onSetRoi256Button(self):
        self.cameraWorkerThread.isSetRoi256ButtonClicked = True
        self.resetRoiButton.setStyleSheet('')
        self.setRoi512Button.setStyleSheet('')
        self.setRoi256Button.setStyleSheet('background-color: green;')
        self.setRoi128Button.setStyleSheet('')

    def onSetRoi128Button(self):
        self.cameraWorkerThread.isSetRoi128ButtonClicked = True
        self.resetRoiButton.setStyleSheet('')
        self.setRoi512Button.setStyleSheet('')
        self.setRoi256Button.setStyleSheet('')
        self.setRoi128Button.setStyleSheet('background-color: green;')

    def onSetNewRoiCenterButton(self):
        try:
            roi_x_center = int(self.roiCenterXEdit.text())
            roi_y_center = int(self.roiCenterYEdit.text())
            self.setCenterSignal.emit(roi_x_center, roi_y_center)
        except ValueError:
            print('*** invalid input in Set new ROI center')
    def onResetRoiCenterButton(self):
        self.cameraWorkerThread.isResetRoiCenterButtonClicked = True

    def onbinning1Button(self):
        self.cameraWorkerThread.isBinning1ButtonClicked = True
        self.binning1Button.setStyleSheet('background-color: green;')
        self.binning2Button.setStyleSheet('')
        self.binning4Button.setStyleSheet('')
        self.binning8Button.setStyleSheet('')

    def onbinning2Button(self):
        self.cameraWorkerThread.isBinning2ButtonClicked = True
        self.binning1Button.setStyleSheet('')
        self.binning2Button.setStyleSheet('background-color: green;')
        self.binning4Button.setStyleSheet('')
        self.binning8Button.setStyleSheet('')

    def onbinning4Button(self):
        self.cameraWorkerThread.isBinning4ButtonClicked = True
        self.binning1Button.setStyleSheet('')
        self.binning2Button.setStyleSheet('')
        self.binning4Button.setStyleSheet('background-color: green;')
        self.binning8Button.setStyleSheet('')

    def onbinning8Button(self):
        self.cameraWorkerThread.isBinning8ButtonClicked = True
        self.binning1Button.setStyleSheet('')
        self.binning2Button.setStyleSheet('')
        self.binning4Button.setStyleSheet('')
        self.binning8Button.setStyleSheet('background-color: green;')
    def onAutomaticFrameScalingCheckbox(self):
        if self.automaticFrameScalingCheckbox.isChecked():
            self.processingThread.rescale_frame_automatically = True
        else:
            self.processingThread.rescale_frame_automatically = False
            try:
                self.processingThread.rescale_frame_min = int(self.frameMinEdit.text())
                print('frame min', self.processingThread.rescale_frame_min)
                self.processingThread.rescale_frame_max = int(self.frameMaxEdit.text())
            except ValueError:
                print('*** invalid input in Set frame min/max')


    def onsetFrameMinMax(self):
        self.processingThread.rescale_frame_automatically = False
        self.automaticFrameScalingCheckbox.setChecked(False)
        try:
            self.processingThread.rescale_frame_min = int(self.frameMinEdit.text())
            self.processingThread.rescale_frame_max = int(self.frameMaxEdit.text())
        except ValueError:
            print('*** invalid input in Set frame min/max')

    def onsetFrameMin(self):
        self.processingThread.rescale_frame_automatically = False
        self.automaticFrameScalingCheckbox.setChecked(False)
        try:
            self.processingThread.rescale_frame_min = int(self.frameMinEdit.text())
        except ValueError:
            print('*** invalid input in Set frame min')

    def onsetFrameMax(self):
        self.processingThread.rescale_frame_automatically = False
        try:
            self.processingThread.rescale_frame_max = int(self.frameMaxEdit.text())
        except ValueError:
            print('*** invalid input in Set frame max')

    def onSetNewCameraSettings(self):
        self.cameraWorkerThread.isSetNewCameraSettingsClicked = True
        try:
            self.camera.exposure_time = float(self.setExposureEdit.text())
            self.camera.gain = int(self.setGainEdit.text())
            self.cameraWorkerThread.nframes_to_grab = int(self.setNFramesToGrab.text())
        except ValueError:
            print('** INVALID INPUT IN SET NEW CAMERA SETTINGS**')
        if self.camera.exposure_time < 0:
            self.camera.exposure_time = 0.1
            print('** negative exposure time!! I set it to 0.1')
        if self.camera.gain < 1:
            self.camera.gain = 1
            print('**camera gain must be an integer between 1 and 4096!! Here < 1, I set it to 1')
        if self.camera.gain > 4096:
            self.camera.gain = 4
            print('**camera gain must be an integer between 1 and 4096!! Here > 4096, I set it to 4')

    def onSaveWhileRunningCheckbox(self):
        if self.saveWhileRunningCheckbox.isChecked():
            self.cameraWorkerThread.save_while_running = True
        else:
            self.cameraWorkerThread.save_while_running = False

    def onSaveWhileSnapOrGrabCheckbox(self):
        if self.saveWhileSnapOrGrabCheckbox.isChecked():
            self.cameraWorkerThread.save_while_snap_or_grab = True
        else:
            self.cameraWorkerThread.save_while_snap_or_grab = False

    def onSaveAlsoRawFrameCheckbox(self):
        if self.saveAlsoRawFrame.isChecked():
            self.processingThread.save_also_raw_frame = True
        else:
            self.processingThread.save_also_raw_frame = False

    def onSaveNpyExtensionCheckbox(self):
        if self.saveNpyExtension.isChecked():
            if 'npy' not in self.processingThread.extensions:
                self.processingThread.extensions.append('npy')
        else:
            if 'npy' in self.processingThread.extensions:
                self.processingThread.extensions.remove('npy')

    def onSavePngExtensionCheckbox(self):
        if self.savePngExtension.isChecked():
            if 'png' not in self.processingThread.extensions:
                self.processingThread.extensions.append('png')
        else:
            if 'png' in self.processingThread.extensions:
                self.processingThread.extensions.remove('png')
    def onSaveTiffExtensionCheckbox(self):
        if self.saveTiffExtension.isChecked():
            if 'tiff' not in self.processingThread.extensions:
                self.processingThread.extensions.append('tiff')
        else:
            if 'tiff' in self.processingThread.extensions:
                self.processingThread.extensions.remove('tiff')

    def onSetMakeNAvgThenSave(self):
        try:
            self.processingThread.make_n_avg_then_save = int(self.setMakeNAvgThenSave.text())
        except ValueError:
            print('*** invalid input in ')
        print('on Set makenavgthen save, now make_n_avg_then_save is ', self.processingThread.make_n_avg_then_save)

    def onSetupSaveDirectory(self):
        self.processingThread.setupDirectoryToSaveFrame(self.processingThread.save_img_dir)
        print('Called setup frame directory')

    def onSelectBackgroundFileButton(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Optional: Set additional options
        file_name, _ = QFileDialog.getOpenFileName(self, "Select background image", self.processingThread.save_img_dir, "All Files (*);;PNG Files (*.png);;Tiff Files (*.tiff);;npy Files (*.npy)", options=options)
        try:
            if file_name:
                print(f'Selected file: {file_name}')
                if file_name.lower().endswith('.npy'):
                    background_image = np.load(file_name)
                    print('Loaded .npy file successfully.', type(background_image), background_image.dtype)
                elif file_name.lower().endswith(('.png', '.tiff')):
                    pil_image = Image.open(file_name)
                    background_image = np.array(pil_image).astype(np.uint16)
                    print('Loaded .png or .tiff file successfully.', type(background_image), background_image.dtype)
                else:
                    print('Unsupported file format.')
        except Exception as e:
            print(f'Error loading image: {e}')
        self.processingThread.background_frame = background_image


    def onSubtractBackgroundCheckbox(self):
        if self.subtractBackgroundCheckbox.isChecked():
            self.processingThread.subtract_background = True
            print('Subtract background to Trues')
        else:
            self.processingThread.subtract_background = False
            print('subtract background to False')

    def onDontPanickButton(self):
        motivational_sentences = {
            1: "If u feel bad, the anatomic department is one stone's trow away. Donate your body to science.",
            2: "Every day may not be good, but there's something good in every day. Look for it?",
            4: "Who is the manager of yourself? Is the position vacant? Can people apply via LinkedIn?",
            5: "The only way to do great work is to love what you do. Or to be held in it by your visa.",
            6: "You are capable of amazing things. Like doing an unscheduled laundry in Switzerland.",
            7: "Two things are endless in life, the PhD and the universe. And sometimes they both really suck.",
            8: "We are just fart of low entropic states in a chaotic soup. Why would you worry then?",
            3: "Your code may have bugs, but so does the universe. You're in good company.",
            9: "You're cooler than an ion! ...",
            10: "... and more repulsive than an ion crystal!",
            11:"In the grand scheme of the universe, your thesis defense is just a small blip. And nobody will read it btw.",
            12: "Every failed experiment is one step closer to discovering something no one else has. Shuttering you to pieces.",
            13: "Life is an optimization problem. If you feel stuck in your local minima, tunnel the f4ck out!",
            14: "Your coffee-to-code ratio might be 1:1, but at least you're caffeinated and confused.",
            15: "Your data might be noisy, but at least it's not as loud as your inner imposter syndrome.",
            16: "Resize the ROI of your life to a smaller scope, and save periodically in the appropriate format.",
            17: "Ehi! Priorities change, it's okay! Anyway, it's getting late"
        }
        sentence = motivational_sentences[np.random.randint(1, len(motivational_sentences) + 1)]
        self.PanicLabel.setText(sentence)
        # try:
        # getCat()
        import urllib.request
        # getCat(self.processingThread.date_directory, 'my_cat', 'png')
        # print('Cat image successfullt imported')
            # self.updateFrameOnGui()
        # except Exception as e:
        # print('Error while catting, ', e)
    def closeEvent(self, event):
        self.camera.close_camera()
        event.accept()

    def onAddMouseLineButton(self):
        if self.addMouseLineButton.isChecked():
            self.processingThread.add_center_line_to_frames = True
        else:
            self.processingThread.add_center_line_to_frames = False

    def onAddCursorsButton(self):
        if self.addCursorsButton.isChecked():
            self.processingThread.add_cursor_xy = True
        else:
            self.processingThread.add_cursor_xy = False
    def onCursorHorizVert(self):
        try:
            self.processingThread.cursor_x_pixels = int(self.CursorHoriz.text())
            self.processingThread.cursor_y_pixels = int(self.CursorVert.text())
            print('curosr x, y', self.processingThread.cursor_y_pixels, self.processingThread.cursor_x_pixels)
        except ValueError:
            print('*** invalid input in cursor horiz/vert')

    def eventFilter(self, obj, event):
        # this function gets the coordinate of your mouse click
        # on the image and saves them to add a line to the frames
        # it rescales by diving for the canvas size and the binning and multiplying by the ROI
        if event.type() == QEvent.MouseButtonPress:
            x = event.x()
            y = event.y()
            self.processingThread.center_line_from_mouse_horiz = int(x/self.canvas.width()*self.camera.roi_current_size[0]/self.camera.binning)
            self.processingThread.center_line_from_mouse_vert = int(y/self.canvas.height()*self.camera.roi_current_size[1]/self.camera.binning)
            # print(f"Mouse moved to ({x}, {y}), but real coordinaes should be ({self.processingThread.center_line_from_mouse_horiz}, {self.processingThread.center_line_from_mouse_vert})")
        return super().eventFilter(obj, event)




class DummyCameraHandler:
    '''
    This class allows you to run the GUI without a camera on the computer.
    It replaced the camera with random stuff from numpy.
    Change the approprite flat in CameraApp

    '''

    def __init__(self, frame_period = 0.001, exposure_time=0.2, gain=2, stabilize_temp=False, binning=1):
        print('In __init__ of DummyCameraHandler')
        self.exposure_time = exposure_time
        self.gain = gain

        # frame dimension and roi size
        self.max_frame_size = [1000, 1000] # CHANGE HERE if camera is different
        self.roi_current_size = self.max_frame_size # init with biggest ROI possible
        self.roi_current_center = [int(self.max_frame_size[0]/2), int(self.max_frame_size[1]/2)] # center of the ROI, by default the center of the frame but can be changed in GUI
        self.roi_default_center = [int(self.max_frame_size[0]/2), int(self.max_frame_size[1]/2)] # default one
        self.frame = np.zeros(self.roi_current_size, dtype=np.uint16)  # init of camera frame
        self.binning = binning # default binning. Available are 2, 4, 8, 16. It can create a last line of dead pixel
        self.roi_size_1000, self.roi_size_512, self.roi_size_256, self.roi_size_128 = [1000, 1000], [512, 512], [256, 256], [128, 128] # neat ROIs
        self.timeout_on_camera = False

        self.set_ROI([1000, 1000], [500, 500])
        self.setup_acquisition()

    @property
    def cam(self):  # this is quite a trick!
        return self

    def open_camera(self):
        print('Camera now is open.')
    def close_camera(self):
        print('...closed.')
    def setup_acquisition(self):
        print('Dummy setup')
    def clear_acquisition(self):
        print('Aquisition Cleared')
    def start_acquisition(self):
        print('Started acquisition...')

    def stop_acquisition(self):
        print('Stopped acquisition...')

    def set_exposure_time(self, exposure_time=None):
        if exposure_time==None: # I changed self.exposure_time from the GUI already
            exposure_time = self.exposure_time
            print('Exposure time from gui', self.exposure_time)
        self.cam.set_exposure(exposure_time)
        self.exposure_time = self.cam.get_exposure()
        print('Now self.exposure_time in CameraHandler is ', self.exposure_time, ' s')

    def set_exposure(self, exposure):
        self.exposure_time = exposure

    def set_gain(self, gain=None):
        if gain == None:
            gain = self.gain
            print('Updating gain from the GUI to ', self.gain)
        self.gain = gain
        print('Dummy gain set to ', self.EMCCD_gain)

    def get_exposure(self):
        return self.exposure_time


    def set_ROI(self, roi_size, roi_center = None, binning=1):
    # self.cam.set_roi takes as arguments hstart, hend, vstart, vend, binning_x, binning_y
        print('in set_ROI, new roi size, new roi center', roi_size, roi_center)
        if not (roi_size[0] % 2 == 0):
            roi_size[0] = roi_size[0] + 1
            print('strecthed roi of one pixel horizontal to make it even, roi_size[0]', roi_size[0])
        if not (roi_size[1] % 2 == 0):
            roi_size[1] = roi_size[1] + 1
            print('strecthed roi of one pixel vertically to make it even. Will crash if alrady 1004, roi_size[1]', roi_size[1])
        if roi_center is not None:
            self.roi_current_center = roi_center
         # check if there is enough space, both when changing the center and when changing the ROI size
        if self.roi_current_center[0] - int(roi_size[0]*0.5) < 0:
            self.roi_current_center[0] = int(roi_size[0]*0.5)
            print('***** new roi center too much on the left, roi size roi center', roi_size, self.roi_current_center, '*****')
        if self.roi_current_center[0] + int(roi_size[0]*0.5) > self.max_frame_size[0]:
            self.roi_current_center[0] = self.max_frame_size[0] - int(roi_size[0]*0.5)
            print('***** new roi center too much on the right, roi size roi center', roi_size, self.roi_current_center, '*****')
        if self.roi_current_center[1] - int(roi_size[1]*0.5) < 0:
            self.roi_current_center[1] = int(roi_size[1]*0.5)
            print('***** new roi center too much on the bottom, roi size roi center', roi_size, self.roi_current_center, '*****')
        if self.roi_current_center[1] + int(roi_size[1]*0.5) > self.max_frame_size[1]:
            self.roi_current_center[1] = self.max_frame_size[1] - int(roi_size[1]*0.5)
            print('***** new roi center too much on the top, roi size roi center', roi_size, self.roi_current_center, '*****')
        self.roi_current_size = roi_size
        self.binning = binning
        hstart = self.roi_current_center[0] - int(self.roi_current_size[0]*0.5)
        hend = self.roi_current_center[0] + int(self.roi_current_size[0]*0.5)
        vstart = self.roi_current_center[1] - int(self.roi_current_size[1]*0.5)
        vend = self.roi_current_center[1] + int(self.roi_current_size[1]*0.5)
        if not isinstance(binning, int) or  not (binning in [1, 2, 4, 8, 16]):
            print('Invalid binning value, I set it to 1. Possible values are 1, 2, 4, 8, 16')
            binning = 1
        # self.cam.set_roi(hstart, hend, vstart, vend, binning, binning)
        # print('camera dget dim', self.cam.get_data_dimensions())
        print('Exiting setRoi, roi_current_size ', self.roi_current_size, 'roi_center', self.roi_current_center)

    def set_binning(self, binning):
        if not isinstance(binning, int) or  not (binning in [1, 2, 4, 8, 16]):
            print('Invalid binning value, I set it to 1. Possible values are 1, 2, 4, 8, 16')
            binning = 1
        print('entering set_binning, self.roi_current_size, self.roi_current_center, self.binning', self.roi_current_size, self.roi_current_center, self.binning)
        self.binning = binning
        hstart = self.roi_current_center[0] - int(self.roi_current_size[0]*0.5)
        hend = self.roi_current_center[0] + int(self.roi_current_size[0]*0.5)
        vstart = self.roi_current_center[1] - int(self.roi_current_size[1]*0.5)
        vend = self.roi_current_center[1] + int(self.roi_current_size[1]*0.5)
        # self.cam.set_roi(hstart, hend, vstart, vend, binning, binning)
        # print('cam.get_data_dimension()', self.cam.get_data_dimensions())
        print('exiting set_binning, self.roi_current_size, self.roi_current_center, self.binning', self.roi_current_size, self.roi_current_center, self.binning)

    def snap(self):
        return np.random.randint(0, 65536, size=[int(self.roi_current_size[0]/self.binning), int(self.roi_current_size[1]/self.binning)], dtype=np.uint16)

    def grab(self, num_frames, return_only_the_avg=True):
        return np.random.randint(0, 65536, size=[int(self.roi_current_size[0]/self.binning), int(self.roi_current_size[1]/self.binning)], dtype=np.uint16)

    def wait_for_frame(self, since='', timeout=''):
        time.sleep(self.exposure_time)

    def read_newest_image(self):
        return np.random.randint(0, 65536, size=[int(self.roi_current_size[0]/self.binning), int(self.roi_current_size[1]/self.binning)], dtype=np.uint16)

    def get_frames_status(self):
        print('Dummy frames are doing great and everything is all right!')

    def read_oldest_image(self):
        return np.random.randint(0, 65536, size=[int(self.roi_current_size[0]/self.binning), int(self.roi_current_size[1]/self.binning)], dtype=np.uint16)
    def acquisition_in_progress(self):
        '''This replaces the self.acquisition_in_progress(), which can throw an error if
        called when cam.close() is already called'''
        try:
            return True
        except Andor.base.AndorError:
            # print('Camera already closed')
            return False
    def is_opened(self):
        return True
    def is_acquisition_setup(self):
        return True
    def acquisition_in_progess(self):
        return True

    def set_frame_period(self, frame_period):
        print('While trying to set_frame_period, I felt sick and went home')


if __name__ == '__main__':
    images_dir = r'C:\Users\Gruppe Willitsch\Documents\data_sw037\images_andor_camera'  # r = raw, fundamental!
    app = QApplication(sys.argv)
    window = CameraApp(verbose=False, dummy_camera=False, dark_theme=True)
    window.show()
    app.aboutToQuit.connect(window.onCloseCamButton)
    sys.exit(app.exec_())
