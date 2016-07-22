from numpy import *
import cv2

img=cv2.imread('ronaldo.jpg',0)
cv2.namedWindow('ronaldo.jpg',cv2.WINDOW_NORMAL)
cv2.imshow('Ronaldo is great',img)
cv2.waitKey(0)
cv2.destroyAllWindows()