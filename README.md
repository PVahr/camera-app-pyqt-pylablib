# camera-app-pyqt-pylablib
A program for scientific cameras supported by pylablib written in PyQt5 for python.
The specific program is implemented for Andor Luca cameras, but you can easily change it to any camera supported by pylablib ([list here](https://pylablib.readthedocs.io/en/latest/devices/cameras_root.html)) and, with a bit more work, possibly to any python-supported scientific camera

## Features
  - livestream of frames at many ROI (size, center), gain, exposure time
  - directly save (png, tiff, npy) the livestream with automatic naming of folder and files via timestamp and settings
  - mouse-based pointer on the frame with additional cursors
  - plots with image integrals and image average in time
  - easily embeed it into your PyQt program for your own experiment
  - naively implemented in numpy: frames are ndarray directly from pylablib
  - a panic button for those really bad, bad days

![Screenshot](img/program_screenshot_darktheme.PNG)

## Usage
1) Install packages:
    - install PyQt5 using pip to the latest version. Versions < 5.12 do not support 16 bit Grayscale format for qimage. Atm the one via conda is < 5.12, so just use 
    - PIL (pillow) for conversion to png, tiff and image manipulation
    - pylablib, of course
    - numpy, datetime, re, sys, os, time
    - qdarkhem if you want the dark theme

2) Run program as main
or else, embeed it into your own PyQt5 program, like
    `from AndorCameraApp import CameraApp`
    `self.myCameraApp = CameraApp()`

3) Change default settings to your taste
   -  in the camera app instance: `verbose=False`, if True prints lots of stuff to console; `dummy_camera=False`, if True runs the program without a physical camera, faking one; `directory_to_save_images=r'./img'` to save your images...; `darktheme=False` to use the dark theme provided by `qdarktheme`
   - default camera exposure time and gain can be changed manually in the init method of the CameraHandler class
   - some other minor default values (like max/min frame intensity, cursor x,y) are defined in the initis metods of the two threads
  
4) Connect the pyqtSignals you might need to the rest of your program
In the `CameraThread` class, you can use `processGrabFrames` to send the frames obtained via `Grab` to your program.
Otherwise, in the `ProcessingThread` class you have the signals `frameSignalToGui`, `horizontalSignal`, `verticalSignal`, `avgSignal` that can be used to send repsectively the whole frame, its integrals horiz/vert, or just the mean of the frame.
This part is still a bit under progress.

## Use with a different camera supported by pylablib
This programs works with Andor Luca, but a little tweaking should make it work with any camera supported by pylablib, as the main functions are the same.

You can start by changing the imports:

`pll.par["devices/dlls/andor_sdk2"] = "C:\Program Files\Andor Driver Pack 2"
from pylablib.devices import Andor`

 and the definition of the `self.cam` variable in the `CameraHandler` class:
 
`self.cam = Andor.AndorSDK2Camera(idx=0, temperature=-20, fan_mode='full')`
to match your camera.

If somes methosds fail, go thorough the `CameraHandler` class and check if methods are missing or working differently.

## Known bugs and limitations
1) Speed and framerate
The measured framerate is less the the given one. When resing the ROI to 512^2 and using some binning, this amounts in around 50 ms of delay for every frame, so quite acceptable.
Is more noticable with bigger frames at full resolution.

Can be in part due to the bandwidth limitation of the Andor Luca tested, in part due to the processing done in Python on the frames themselves.
The processing is implemented via multithreading, but the multithreading of PyQt and Python in general does not allow to use different physical cores, resulting in an accumulation of times (the time to acquire the frame + to process it).
At small roi and binning the framerate is fast enough (fastest doable with Luca is 50 ms, after which the GUI start to slow down coniderably).

2) Sending frames to another PyQt5 program
Still not sure about which pyqSignal to use and where. The possible signals are listed above, but there is a bit of confusion.

## Code structures



