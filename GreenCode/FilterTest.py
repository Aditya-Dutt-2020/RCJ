import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
def nothing(x):
    pass


cv2.createTrackbar('HH',"Trackbars", 91, 400, nothing)
cv2.createTrackbar('SH',"Trackbars", 400, 400, nothing)
cv2.createTrackbar('VH',"Trackbars", 220, 400, nothing)
cv2.createTrackbar('HL',"Trackbars", 61, 400, nothing)
cv2.createTrackbar('SL',"Trackbars", 164, 400, nothing)
cv2.createTrackbar('VL',"Trackbars", 0, 400, nothing)

while(1):
    _, frame = cap.read()
#    frame = cv2.imread("greenFilter.jpg")
    #height, width = frame.shape[:2]
    #frame = cv2.resize(frame, (math.floor(0.1*width),math.floor(0.1*height)), interpolation = cv2.INTER_CUBIC)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    HH = cv2.getTrackbarPos('HH',"Trackbars")
    HS = cv2.getTrackbarPos('SH',"Trackbars")
    HV = cv2.getTrackbarPos('VH',"Trackbars")
    LH = cv2.getTrackbarPos('HL',"Trackbars")
    LS = cv2.getTrackbarPos('SL',"Trackbars")
    LV = cv2.getTrackbarPos('VL',"Trackbars")
    lower_green = np.array([LH,LS,LV])
    upper_green = np.array([HH,HS,HV])
#    lower_red = np.array([LH, LS, LV])
#    upper_red = np.array([HH, HS, HV])   
    mask = cv2.inRange(hsv, lower_green, upper_green)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()