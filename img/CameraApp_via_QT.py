# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CameraApp_via_QT.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CameraAppGUI(object):
    def setupUi(self, CameraAppGUI):
        CameraAppGUI.setObjectName("CameraAppGUI")
        CameraAppGUI.setWindowModality(QtCore.Qt.WindowModal)
        CameraAppGUI.resize(1421, 774)
        CameraAppGUI.setFocusPolicy(QtCore.Qt.ClickFocus)
        CameraAppGUI.setDocumentMode(True)
        CameraAppGUI.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(CameraAppGUI)
        self.centralwidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.centralwidget.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.canvas = QtWidgets.QLabel(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.canvas.setMouseTracking(True)
        self.canvas.setText("")
        self.canvas.setPixmap(QtGui.QPixmap("2024_01_17_00000_16.15.15.362_im_s_exp0.1_gain2.png"))
        self.canvas.setScaledContents(True)
        self.canvas.setObjectName("canvas")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(570, 0, 429, 111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.camera_run_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.camera_run_layout.setContentsMargins(0, 0, 0, 0)
        self.camera_run_layout.setObjectName("camera_run_layout")
        self.snapButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.snapButton.setObjectName("snapButton")
        self.camera_run_layout.addWidget(self.snapButton, 0, 2, 1, 1)
        self.startAcqui = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.startAcqui.setObjectName("startAcqui")
        self.camera_run_layout.addWidget(self.startAcqui, 0, 0, 1, 1)
        self.clearPlotButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.clearPlotButton.setObjectName("clearPlotButton")
        self.camera_run_layout.addWidget(self.clearPlotButton, 0, 4, 1, 1)
        self.grabButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.grabButton.setObjectName("grabButton")
        self.camera_run_layout.addWidget(self.grabButton, 0, 3, 1, 1)
        self.stopAcqui = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.stopAcqui.setObjectName("stopAcqui")
        self.camera_run_layout.addWidget(self.stopAcqui, 0, 1, 1, 1)
        self.setupAcqui = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.setupAcqui.setObjectName("setupAcqui")
        self.camera_run_layout.addWidget(self.setupAcqui, 1, 0, 1, 1)
        self.clearAcqui = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.clearAcqui.setEnabled(True)
        self.clearAcqui.setCheckable(False)
        self.clearAcqui.setObjectName("clearAcqui")
        self.camera_run_layout.addWidget(self.clearAcqui, 1, 1, 1, 1)
        self.openCam = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.openCam.setEnabled(True)
        self.openCam.setObjectName("openCam")
        self.camera_run_layout.addWidget(self.openCam, 1, 2, 1, 1)
        self.closeCam = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.closeCam.setEnabled(False)
        self.closeCam.setObjectName("closeCam")
        self.camera_run_layout.addWidget(self.closeCam, 1, 3, 1, 1)
        self.restartCameraThreadButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.restartCameraThreadButton.setEnabled(False)
        self.restartCameraThreadButton.setObjectName("restartCameraThreadButton")
        self.camera_run_layout.addWidget(self.restartCameraThreadButton, 1, 4, 1, 1)
        self.camera_settings_group_box = QtWidgets.QGroupBox(self.centralwidget)
        self.camera_settings_group_box.setGeometry(QtCore.QRect(570, 120, 551, 121))
        self.camera_settings_group_box.setObjectName("camera_settings_group_box")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.camera_settings_group_box)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 20, 505, 96))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.setNFramesToGrab = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setNFramesToGrab.sizePolicy().hasHeightForWidth())
        self.setNFramesToGrab.setSizePolicy(sizePolicy)
        self.setNFramesToGrab.setObjectName("setNFramesToGrab")
        self.gridLayout.addWidget(self.setNFramesToGrab, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.setExposureEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setExposureEdit.sizePolicy().hasHeightForWidth())
        self.setExposureEdit.setSizePolicy(sizePolicy)
        self.setExposureEdit.setObjectName("setExposureEdit")
        self.gridLayout.addWidget(self.setExposureEdit, 0, 2, 1, 1)
        self.setNewCameraSettings = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.setNewCameraSettings.setObjectName("setNewCameraSettings")
        self.gridLayout.addWidget(self.setNewCameraSettings, 2, 1, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.subtractBackgroundCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.subtractBackgroundCheckbox.setObjectName("subtractBackgroundCheckbox")
        self.gridLayout.addWidget(self.subtractBackgroundCheckbox, 1, 3, 1, 1)
        self.setGainEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setGainEdit.sizePolicy().hasHeightForWidth())
        self.setGainEdit.setSizePolicy(sizePolicy)
        self.setGainEdit.setObjectName("setGainEdit")
        self.gridLayout.addWidget(self.setGainEdit, 0, 4, 1, 1)
        self.selectBackgroundFileButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.selectBackgroundFileButton.setObjectName("selectBackgroundFileButton")
        self.gridLayout.addWidget(self.selectBackgroundFileButton, 1, 4, 1, 1)
        self.roi_settings_group_box = QtWidgets.QGroupBox(self.centralwidget)
        self.roi_settings_group_box.setGeometry(QtCore.QRect(570, 260, 571, 211))
        self.roi_settings_group_box.setObjectName("roi_settings_group_box")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.roi_settings_group_box)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(-1, 19, 571, 191))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.ROI_settings_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.ROI_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.ROI_settings_layout.setObjectName("ROI_settings_layout")
        self.setFrameMinMax = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setFrameMinMax.sizePolicy().hasHeightForWidth())
        self.setFrameMinMax.setSizePolicy(sizePolicy)
        self.setFrameMinMax.setObjectName("setFrameMinMax")
        self.ROI_settings_layout.addWidget(self.setFrameMinMax, 3, 6, 1, 1)
        self.frameMinEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameMinEdit.sizePolicy().hasHeightForWidth())
        self.frameMinEdit.setSizePolicy(sizePolicy)
        self.frameMinEdit.setObjectName("frameMinEdit")
        self.ROI_settings_layout.addWidget(self.frameMinEdit, 3, 3, 1, 1)
        self.frameMaxEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameMaxEdit.sizePolicy().hasHeightForWidth())
        self.frameMaxEdit.setSizePolicy(sizePolicy)
        self.frameMaxEdit.setObjectName("frameMaxEdit")
        self.ROI_settings_layout.addWidget(self.frameMaxEdit, 3, 5, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.ROI_settings_layout.addWidget(self.label_11, 3, 4, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.ROI_settings_layout.addWidget(self.label_10, 3, 2, 1, 1)
        self.binning8Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.binning8Button.sizePolicy().hasHeightForWidth())
        self.binning8Button.setSizePolicy(sizePolicy)
        self.binning8Button.setObjectName("binning8Button")
        self.ROI_settings_layout.addWidget(self.binning8Button, 1, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.ROI_settings_layout.addWidget(self.label_8, 2, 4, 1, 1)
        self.setNewRoiCenterButton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setNewRoiCenterButton.sizePolicy().hasHeightForWidth())
        self.setNewRoiCenterButton.setSizePolicy(sizePolicy)
        self.setNewRoiCenterButton.setObjectName("setNewRoiCenterButton")
        self.ROI_settings_layout.addWidget(self.setNewRoiCenterButton, 2, 6, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.ROI_settings_layout.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.ROI_settings_layout.addWidget(self.label_4, 0, 0, 1, 1)
        self.setRoi256Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.setRoi256Button.setObjectName("setRoi256Button")
        self.ROI_settings_layout.addWidget(self.setRoi256Button, 0, 3, 1, 1)
        self.automaticFrameScalingCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.automaticFrameScalingCheckbox.sizePolicy().hasHeightForWidth())
        self.automaticFrameScalingCheckbox.setSizePolicy(sizePolicy)
        self.automaticFrameScalingCheckbox.setObjectName("automaticFrameScalingCheckbox")
        self.ROI_settings_layout.addWidget(self.automaticFrameScalingCheckbox, 3, 1, 1, 1)
        self.roiCenterXEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.roiCenterXEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roiCenterXEdit.sizePolicy().hasHeightForWidth())
        self.roiCenterXEdit.setSizePolicy(sizePolicy)
        self.roiCenterXEdit.setObjectName("roiCenterXEdit")
        self.ROI_settings_layout.addWidget(self.roiCenterXEdit, 2, 3, 1, 1)
        self.binning2Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.binning2Button.sizePolicy().hasHeightForWidth())
        self.binning2Button.setSizePolicy(sizePolicy)
        self.binning2Button.setObjectName("binning2Button")
        self.ROI_settings_layout.addWidget(self.binning2Button, 1, 2, 1, 1)
        self.setRoi128Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.setRoi128Button.setObjectName("setRoi128Button")
        self.ROI_settings_layout.addWidget(self.setRoi128Button, 0, 4, 1, 1)
        self.binning1Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.binning1Button.setObjectName("binning1Button")
        self.ROI_settings_layout.addWidget(self.binning1Button, 1, 1, 1, 1)
        self.setRoi512Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setRoi512Button.sizePolicy().hasHeightForWidth())
        self.setRoi512Button.setSizePolicy(sizePolicy)
        self.setRoi512Button.setObjectName("setRoi512Button")
        self.ROI_settings_layout.addWidget(self.setRoi512Button, 0, 2, 1, 1)
        self.binning4Button = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.binning4Button.setObjectName("binning4Button")
        self.ROI_settings_layout.addWidget(self.binning4Button, 1, 3, 1, 1)
        self.resetRoiButton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.resetRoiButton.setObjectName("resetRoiButton")
        self.ROI_settings_layout.addWidget(self.resetRoiButton, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_6.setObjectName("label_6")
        self.ROI_settings_layout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.ROI_settings_layout.addWidget(self.label_7, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.ROI_settings_layout.addWidget(self.label_5, 1, 0, 1, 1)
        self.roiCenterYEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roiCenterYEdit.sizePolicy().hasHeightForWidth())
        self.roiCenterYEdit.setSizePolicy(sizePolicy)
        self.roiCenterYEdit.setObjectName("roiCenterYEdit")
        self.ROI_settings_layout.addWidget(self.roiCenterYEdit, 2, 5, 1, 1)
        self.resetRoiCenterButton = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.resetRoiCenterButton.setObjectName("resetRoiCenterButton")
        self.ROI_settings_layout.addWidget(self.resetRoiCenterButton, 2, 1, 1, 1)
        self.addMouseLineButton = QtWidgets.QCheckBox(self.gridLayoutWidget_3)
        self.addMouseLineButton.setObjectName("addMouseLineButton")
        self.ROI_settings_layout.addWidget(self.addMouseLineButton, 4, 1, 1, 1)
        self.addCursorsButton = QtWidgets.QCheckBox(self.gridLayoutWidget_3)
        self.addCursorsButton.setObjectName("addCursorsButton")
        self.ROI_settings_layout.addWidget(self.addCursorsButton, 4, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.ROI_settings_layout.addWidget(self.label_13, 4, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.ROI_settings_layout.addWidget(self.label_14, 4, 5, 1, 1)
        self.CursorHoriz = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CursorHoriz.sizePolicy().hasHeightForWidth())
        self.CursorHoriz.setSizePolicy(sizePolicy)
        self.CursorHoriz.setObjectName("CursorHoriz")
        self.ROI_settings_layout.addWidget(self.CursorHoriz, 4, 4, 1, 1)
        self.CursorVert = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CursorVert.sizePolicy().hasHeightForWidth())
        self.CursorVert.setSizePolicy(sizePolicy)
        self.CursorVert.setObjectName("CursorVert")
        self.ROI_settings_layout.addWidget(self.CursorVert, 4, 6, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(570, 530, 571, 161))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 30, 571, 131))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dontPanickButton = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.dontPanickButton.setObjectName("dontPanickButton")
        self.gridLayout_2.addWidget(self.dontPanickButton, 2, 0, 1, 6)
        self.saveTiffExtension = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.saveTiffExtension.setObjectName("saveTiffExtension")
        self.gridLayout_2.addWidget(self.saveTiffExtension, 0, 5, 1, 1)
        self.savePngExtension = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.savePngExtension.setObjectName("savePngExtension")
        self.gridLayout_2.addWidget(self.savePngExtension, 0, 4, 1, 1)
        self.saveWhileRunningCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.saveWhileRunningCheckbox.setObjectName("saveWhileRunningCheckbox")
        self.gridLayout_2.addWidget(self.saveWhileRunningCheckbox, 0, 0, 1, 1)
        self.saveNpyExtension = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.saveNpyExtension.setObjectName("saveNpyExtension")
        self.gridLayout_2.addWidget(self.saveNpyExtension, 0, 3, 1, 1)
        self.saveWhileSnapOrGrabCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.saveWhileSnapOrGrabCheckbox.setObjectName("saveWhileSnapOrGrabCheckbox")
        self.gridLayout_2.addWidget(self.saveWhileSnapOrGrabCheckbox, 0, 1, 1, 1)
        self.saveAlsoRawFrame = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.saveAlsoRawFrame.setObjectName("saveAlsoRawFrame")
        self.gridLayout_2.addWidget(self.saveAlsoRawFrame, 0, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 0, 1, 1)
        self.SetupSaveDirectory = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.SetupSaveDirectory.setObjectName("SetupSaveDirectory")
        self.gridLayout_2.addWidget(self.SetupSaveDirectory, 1, 2, 1, 1)
        self.setMakeNAvgThenSave = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setMakeNAvgThenSave.sizePolicy().hasHeightForWidth())
        self.setMakeNAvgThenSave.setSizePolicy(sizePolicy)
        self.setMakeNAvgThenSave.setObjectName("setMakeNAvgThenSave")
        self.gridLayout_2.addWidget(self.setMakeNAvgThenSave, 1, 1, 1, 1)
        self.PanicLabel = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.PanicLabel.setObjectName("PanicLabel")
        self.gridLayout_2.addWidget(self.PanicLabel, 3, 0, 1, 6)
        self.plot_bottom = PlotWidget(self.centralwidget)
        self.plot_bottom.setGeometry(QtCore.QRect(0, 510, 501, 41))
        self.plot_bottom.setObjectName("plot_bottom")
        self.plot_avg = PlotWidget(self.centralwidget)
        self.plot_avg.setGeometry(QtCore.QRect(0, 560, 501, 141))
        self.plot_avg.setObjectName("plot_avg")
        self.plot_right = PlotWidget(self.centralwidget)
        self.plot_right.setGeometry(QtCore.QRect(510, 0, 51, 501))
        self.plot_right.setObjectName("plot_right")
        CameraAppGUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CameraAppGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1421, 21))
        self.menubar.setObjectName("menubar")
        CameraAppGUI.setMenuBar(self.menubar)

        self.retranslateUi(CameraAppGUI)
        QtCore.QMetaObject.connectSlotsByName(CameraAppGUI)

    def retranslateUi(self, CameraAppGUI):
        _translate = QtCore.QCoreApplication.translate
        CameraAppGUI.setWindowTitle(_translate("CameraAppGUI", "Un giorno alla volta"))
        self.snapButton.setText(_translate("CameraAppGUI", "Snap"))
        self.startAcqui.setText(_translate("CameraAppGUI", "Start acq"))
        self.clearPlotButton.setText(_translate("CameraAppGUI", "Clear plot"))
        self.grabButton.setText(_translate("CameraAppGUI", "Grab"))
        self.stopAcqui.setText(_translate("CameraAppGUI", "Stop acq"))
        self.setupAcqui.setText(_translate("CameraAppGUI", "Setup acq"))
        self.clearAcqui.setText(_translate("CameraAppGUI", "Clear acq"))
        self.openCam.setText(_translate("CameraAppGUI", "Open cam"))
        self.closeCam.setText(_translate("CameraAppGUI", "Close cam"))
        self.restartCameraThreadButton.setText(_translate("CameraAppGUI", "Restart cam thread"))
        self.camera_settings_group_box.setTitle(_translate("CameraAppGUI", "Camera settings"))
        self.label.setText(_translate("CameraAppGUI", "Exposure time\n"
"(s)"))
        self.label_3.setText(_translate("CameraAppGUI", "set N frames to \n"
" grab when Grab"))
        self.setNewCameraSettings.setText(_translate("CameraAppGUI", "Set new camera settings"))
        self.label_2.setText(_translate("CameraAppGUI", "gain\n"
"(1 to 4096)"))
        self.subtractBackgroundCheckbox.setText(_translate("CameraAppGUI", "Subtract\n"
"background"))
        self.selectBackgroundFileButton.setText(_translate("CameraAppGUI", "select background"))
        self.roi_settings_group_box.setTitle(_translate("CameraAppGUI", "ROI settings"))
        self.setFrameMinMax.setText(_translate("CameraAppGUI", "Set frame\n"
"min/max"))
        self.label_11.setText(_translate("CameraAppGUI", "Frame max\n"
"(Enter to set)"))
        self.label_10.setText(_translate("CameraAppGUI", "Frame min\n"
"(Enter to set)"))
        self.binning8Button.setText(_translate("CameraAppGUI", "8"))
        self.label_8.setText(_translate("CameraAppGUI", "Y center\n"
"(Enter to set)"))
        self.setNewRoiCenterButton.setText(_translate("CameraAppGUI", "Set new"))
        self.label_9.setText(_translate("CameraAppGUI", "Frame rescaling\n"
"(0 to 65535, 16 bit)"))
        self.label_4.setText(_translate("CameraAppGUI", "ROI size"))
        self.setRoi256Button.setText(_translate("CameraAppGUI", "256*256"))
        self.automaticFrameScalingCheckbox.setText(_translate("CameraAppGUI", "Auto"))
        self.binning2Button.setText(_translate("CameraAppGUI", "2"))
        self.setRoi128Button.setText(_translate("CameraAppGUI", "128*128"))
        self.binning1Button.setText(_translate("CameraAppGUI", "None"))
        self.setRoi512Button.setText(_translate("CameraAppGUI", "512*512"))
        self.binning4Button.setText(_translate("CameraAppGUI", "4"))
        self.resetRoiButton.setText(_translate("CameraAppGUI", "1000*1000"))
        self.label_6.setText(_translate("CameraAppGUI", "ROI center"))
        self.label_7.setText(_translate("CameraAppGUI", "X center\n"
"(Enter to set)"))
        self.label_5.setText(_translate("CameraAppGUI", "Binning"))
        self.resetRoiCenterButton.setText(_translate("CameraAppGUI", "Reset"))
        self.addMouseLineButton.setText(_translate("CameraAppGUI", "add cross\n"
"at mouse\n"
"pos"))
        self.addCursorsButton.setText(_translate("CameraAppGUI", "add x, y\n"
"cursors"))
        self.label_13.setText(_translate("CameraAppGUI", "+- ... pixels\n"
"horiz\n"
"(Enter to set)"))
        self.label_14.setText(_translate("CameraAppGUI", "+- ... pixels\n"
"vert\n"
"(Enter to set)"))
        self.groupBox.setTitle(_translate("CameraAppGUI", "Saving settings"))
        self.dontPanickButton.setText(_translate("CameraAppGUI", "Panic! Save myself instead of the pictures!"))
        self.saveTiffExtension.setText(_translate("CameraAppGUI", "save .tiff"))
        self.savePngExtension.setText(_translate("CameraAppGUI", "save .png"))
        self.saveWhileRunningCheckbox.setText(_translate("CameraAppGUI", "save while\n"
"running"))
        self.saveNpyExtension.setText(_translate("CameraAppGUI", "save .npy"))
        self.saveWhileSnapOrGrabCheckbox.setText(_translate("CameraAppGUI", "save while\n"
"snap, grab"))
        self.saveAlsoRawFrame.setText(_translate("CameraAppGUI", "Save also raw\n"
"(unrescaled) frame"))
        self.label_12.setText(_translate("CameraAppGUI", "Make N avg\n"
"then save\n"
"(press Enter)"))
        self.SetupSaveDirectory.setText(_translate("CameraAppGUI", "Reset save folder"))
        self.PanicLabel.setText(_translate("CameraAppGUI", "**AHHHHH** HELP"))
from pyqtgraph import PlotWidget
