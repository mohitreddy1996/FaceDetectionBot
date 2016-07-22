import cv2
from numpy import *

cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)
while True:
	
	ret,frame = cap.read()
	if ret == False :
		print "wrong"
		break
	cv2.namedWindow('frames',cv2.WINDOW_NORMAL)
	#gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#cv2.imshow('frames',gray)
	cv2.imshow('frames',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()