# camera-app-pyqt-pylablib
A program for scientific cameras supported by pylablib written in PyQt5 for python.
The specific program is implemented for Andor Luca cameras, but you can easily changed o any camera supported by pylablib ([list here](https://pylablib.readthedocs.io/en/latest/devices/cameras_root.html)) and, with a bit more work, possibly to any python-supported scientific camera

## Features
  - livestream of frames at many ROI (size, center), gain, exposure time
  - directly save (png, tiff, npy) the livestream with automatic naming of folder and files via timestamp and settings
  - mouse-based pointer on the frame with additional cursors
  - plots with image integrals and image average in time
  - easily embeed it into your PyQt program for your own experiment
  - a panic button for those really bad, bad days

[image](img/program_screenshot_darktheme.PNG)

## Usage

#### packages
- install PyQt5 using pip to the latest version. Versions < 5.12 do not support 16 bit Grayscale format for qimage. Atm the one via conda is < 5.12
- PIL (pillow) for conversion to png, tiff and image manipulation
- pylablib, of course
- numpy, datetime, re, sys, os, time

## Use with a different camera

## Code structures

## Known bugs and limitations

