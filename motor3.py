import cv2,numpy as np
from PIL import Image
from math import sin, cos, radians
import time
import RPi.GPIO as GPIO 
from time import sleep 

GPIO.setmode(GPIO.BOARD)
#print "1"
Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 29
Motor2B = 31
Motor2E = 33

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
#print "2"
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
#print "3"
def left():
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.HIGH)
	sleep(1)
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)

def right():
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
	sleep(1)
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)

#print "4"
camera =  cv2.VideoCapture(0)
face = cv2.CascadeClassifier("/home/pi/haarcascade_frontalface_alt2.xml")

#print "5"
settings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 3, 
    'minSize': (50, 50), 
    'flags': cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT|cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]
xo=0
yo=0
xn=0
yn=0
#print "6"
while camera.isOpened():
    ret, img = camera.read()
    if ret==False:
	continue
    #print "7"
    cv2.imshow('facedetect', img)
    r,c,s = img.shape
    for angle in [0,-10,-20,-30,10,20,30]:
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        if len(detected):
            detected = [rotate_point(detected[-1], img, -angle)]
	   # print angle
            break
    #print "8"
    # Make a copy as we don't want to draw on the original image:
    for x, y, w, h in detected[-1:]:
	#print x,y,w,h
        xn=x
        yn=y
        cv2.rectangle(img, (x, y), (x+h, y+w), (255,0,0), 2)
	n=0
    if( (xo !=0 or yo !=0) and (xo!=xn or yo!=yn)):
        print xo,yo
        print xn,yn
        if(xo<=xn and yn<= yo and xn-xo >= yo-yn):
            #print "Going Right slightly Top"
	    right()
        elif( xo <=xn and yo<=yn and xn-xo < yo-yn):
            print "Going Top slightly Right"
            #right()
        elif( xo <= xn and yn>=yo and xn-xo >= yn-yo):
            #print "Going Right slightly Bottom"
            right()
        elif( xo <= xn and yn>= yo and xn-xo < yn-yo):
            print "Going Bottom slightly Right"
            #right()
        elif( xo >= xn and yo <=yn and xo-xn >=yn-yo):
            #print "Going Left slightly Bottom"
	    left() #adsf
        elif( xo >=xn and yo <= yn and xo-xn < yn-yo):
            print "Going Bottom slightly Left"
	    #left() #aqwr
        elif( xo>=xn and yo >=yn and xo-xn >= yo-yn):
            #print "Going Left slightly Top"
	    left() #aweg
        elif(xo>=xn and yo >=yn and xo-xn < yo-yn):
            print "Going Top slightly Left"
            #left() #qrer
        
                  
                       
    '''now = time.time()
    #print now
    future= now + 0.001
    while True:
        if time.time() > future:
            break    '''
   
    xo=xn
    yo=yn




    if cv2.waitKey(5) != -1:
        break
GPIO.output(Motor1E,GPIO.LOW)
GPIO.output(Motor2E,GPIO.LOW)
cv2.destroyWindow("facedetect")
GPIO.cleanup()
