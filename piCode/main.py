import greenDetectAditya
import greenDetectBrian
import ballDetectionBrian

import serialPi
import buttonStopper as bs
import piCam

import sys
import numpy as np
import cv2

'''
while not cap.isOpened():
    cap = cv2.VideoCapture(0)
'''

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
serialPi.initSerial()


#initalize button thing
bs.initButton()

#initalize pi cam
piCam.initialize()


progStop = False
inRescueRoom = False

while(True):
    #button stop code
    if bs.getButton():
        progStop = not progStop
        if not progStop:
            serialPi.write("cont")
        else:
            serialPi.write("stop")
    if progStop:
        continue
    
    #get frame from camera
    frame=piCam.getframe()
    
    
    #rescue room stuff
    
    #check if currently in rescue room
    if inRescueRoom:
        cx,cy,area,BorS = ballDetectionBrian.ballDetect(frame) #cx cy area and BorS are all arrays that correspond with eachother
        #do stuff
        
        continue
    
    #check if entering rescue room
    if silverTapeBrian.silverCheck()
        inRescueRoom=True
        serialPi.write("raise camera")
        continue
    
    #green square stuff
    #move = greenDetectAditya.detectGreen(frame)
    move = greenDetectBrian.detectGreen(frame)
    if move != "skip":
        serialPi.write("stop")
        if move == "U":
            serialPi.write("turn180l")
        elif move == "left":
            serialPi.write("turn090l")
        elif move == "right":
            serialPi.write("turn090r")
        serialPi.write("cont")


# Some how end program.
piCam.endprogram()
