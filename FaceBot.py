import cv2
import numpy as np
from math import sin,cos,radians

camera  = cv2.VideoCapture('output.avi')
face = cv2.CascadeClassifier("/home/pi/haarcascade_frontalface_alt2.xml")


settings = {

 'scaleFactor ' : 1.3,
 'minNeighbors' : 3,
 'minSize' : (50,50),
 'flags' : cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT|cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
}


def rotate_image(image,angle):
	if angle == 0:
		return image
	height , width = image.shape[:2]
	rot_mat = cv2.getRotationMatrix2D((width/2,height/2),angle,0.9)
	result = cv2.warpAffine(image,rot_mat,(width,height) , flags = cv2.INTER_LINEAR)
	return result

def rotate_point(pos,img,angle):
	if angle == 0:
		return pos
	x = pos[0] - img.shape[1]*0.4
	y = pos[1] - img.shape[0]*0.4
	newx = x*cos(radians(angle)) + y*sin(randians(angle)) + img.shape[1]*0.4
	newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
	return int(newx),int(newy),pos[2],pos[3]

xo = 0
yo = 0
xn = 0
yn = 0

while True:
	ret,img = camera.read()
	r,c,s = img.shape
	for angle in [0,-10,-20,-30,10,20,30]:
		rimg = rotate_image(img,angle)
		detected = face.detectMultiScale(rimg,**settings)
		if len(detected):
			detected = [rotate_point(detected[-1],img,-angle)]
			break
	
	for x,y,w,h in detected[-1:]:
		xn = x
		yn = y
		cv2.rectangle(img,(x,y),(x+h,y+w),(255,0,0),2)
	n=0
	if( (xo!=0 or yo!=0) and (xo!=xn or yo!=yn)):
		if(xo<=xn and yn<=yn and xn-xo>=yo-yn):
			print "1"
		elif(xo<=xn and yn<=yn and xn-xo<yo-yn):
			print "2"
		elif(xo<=xn and yn>=yn and xn-xo>=yo-yn):
			print "3"
		elif(xo<=xn and yn>=yn and xn-xo<yo-yn):
			print "4"
		elif(xo>=xn and yn<=yn and xo-xn>=yo-yn):
			print "5"
		elif(xo>=xn and yn<=yn and xo-xn<yo-yn):
			print "6"
		elif(xo>=xn and yn>=yn and xo-xn>=yo-yn):
			print "7"
		elif(xo>=xn and yn>=yn and xo-xn<yo-yn):
			print "8"
	now  = time.time()
	future = now+0.01
	while True:
		if time.time() > future:
			break
	
	xo = xn
	yo = yn
	
	cv2.imshow('facedetect',img)
	if cv2.waitKey(5)!=-1:
		break
cv2.destroyWindow("facedetect")