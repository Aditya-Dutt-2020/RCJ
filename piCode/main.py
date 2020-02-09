import greenDetectAditya
import greenDetectBrian
import ballDetectionBrian
import silverTapeBrian

import sys
import numpy as np
import cv2
import time
import serial
import RPi.GPIO as GPIO

while not cap.isOpened():
    cap = cv2.VideoCapture(0)


'''
def hsvcontours(frame, hl, hh, sl, sh, vl, vh):
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsvlow  = np.array([hl, sl, vl])
    hsvhigh = np.array([hh, sh, vh])
    mask = cv2.inRange(hsvframe, hsvlow, hsvhigh)
    _, contours, h = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def hsvinversecontours(frame, hl, hh, sl, sh, vl, vh):
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsvlow  = np.array([hl, sl, vl])
    hsvhigh = np.array([hh, sh, vh])
    mask = cv2.inRange(hsvframe, hsvlow, hsvhigh)
    mask = cv2.bitwise_not(mask)
    _, contours, h = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours
'''

#initalize serial
global s1
s1 = serial.Serial('COM6', 115200)
s1.flushInput()
def serialwrite(code)
    s1.write(str.encode(code))
    print("serial write: "+code)

#initalize button thing
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def getbutton():
    return not GPIO.input(18)


progStop = False
inRescueRoom = False

while(cap.isOpened()):
    #button stop code
    if getbutton():
        progStop = not progStop
        if not progStop:
            serialwrite("cont")
        else:
            serialwrite("stop")
    if progStop:
        continue
    
    #get frame from camera
    ret,frame=cap.read()
    if not ret:
        print("ret error")
        continue
    
    #rescue room stuff
    
    #check if currently in rescue room
    if inRescueRoom:
        cx,cy,area = ballDetectionBrian.ballDetect(frame) #cx cy and area are all arrays that correspond with eachother
        #do stuff
        
        continue
    
    #check if entering rescue room
    if silverTapeBrian.silverCheck()
        inRescueRoom=True
        serialwrite("raise camera")
        continue
    
    #green square stuff
    #move = greenDetectAditya.detectGreen(frame)
    move = greenDetectBrian.detectGreen(frame)
    if move != "skip":
        serialwrite("stop")
        if move == "U":
            serialwrite("turn180l")
        elif move == "left":
            serialwrite("turn090l")
        elif move == "right":
            serialwrite("turn090r")
        serialwrite("cont")


# Some how end program.
cap.release()
cv2.destroyAllWindows()

