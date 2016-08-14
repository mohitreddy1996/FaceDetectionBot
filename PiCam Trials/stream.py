from picamera import *
from time import sleep
from imgproc import *


camera=Camera(720,1280)
viewer=Viewer(720,1280,"SUDO_AC")
count=0
while count<=10000:
	img=camera.grabImage()
	viewer.displayImage(img)
	waitTime(1)
	count=count+1
	
	