from picamera import *
from time import *

camera=PiCamera()
camera.start_preview()
camera.resolution = (240,180)
camera.start_recording('second.h264')
sleep(5)
camera.stop_recording()

'''import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.cv.CV_FOURCC(*'XVID')

out = cv2.VideoWriter('out.avi',fourcc,20.0,(

'''