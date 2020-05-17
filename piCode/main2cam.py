'''
NOTE! WIP! This code assumes that there are two cameras. One in the front and one in the back.
The camera on the back should be on a servo, while the one in the front faces down.
These are the following serial messages that I use:
cameraup = turn camera up
cameradown = turn camera down
openclaw = open the claw
closeclaw = close claw
piCam is the camera module we made.
piCam.getFrame(camindex) gets the frame of whatever camera we want
camindex 0 is the front camera
camindex 1 is the back camera
'''


import greenDetect
import ballDetect

import serialPi
import buttonStopper as bs
import detectTriangle
import piCam

import sys
import numpy as np
import cv2


def main():
    serialPi.initSerial()
    bs.initButton()
    piCam.initialize()

    progStop = False
    inBallRoom = False
    foundBall = False
    grabbedBall = False
    foundtr = False
    lastdist = 0

    while True:
        if bs.getButton():
            progStop = not progStop
            if progStop == False:
                serialPi.write("cont")
            else:
                serialPi.write("stop")
        if progStop:
            continue

        frame = piCam.getFrame(0)
        frame2 = piCam.getFrame(1)

        serialPi.write("stop")

        if inBallRoom:
            if foundtr:
                serialPi.write("camerdown")
                grabbedBall = False
                serialPi.write("move001b")
                thresh = cv2.threshold(frame2, 130, 255, cv2.THRESH_BINARY)
                if len(thresh[np.where(thresh==0)]) > frame2.shape[0]*frame2.shape[1]//2:
                    serailPi.write("openclaw")
                    continue
            
            if grabbedBall:
                serialPi.write("cameraup")
                foundBall = False
                x, y, tr = detectTriangle(frame2)
                if not tr:
                    serialPi.write("turn001l")
                else:
                    leverage = 10
                    if width/2-leverage < x < width/2+leverage:
                        serialPi.write("move001b")
                        foundtr = True
                    elif x < width/2:
                        serialPi.write("turn005r")
                    elif x > width/2:
                        serialPi.write("turn005l")
                continue
                        
            if foundBall:
                serialPi.write("cameradown")
                serialPi.write("move001b")
                _,_,r,_ = ballDetect.ballDetect(frame2)
                if len(r) > 0:
                    serialPi.write("move003b")
                    serialPi.write("closeclaw")
                    grabbedBall = True
                continue
            
            cx,cy,r,silver = ballDetect.ballDetect(frame2)
            numballs = len(r)
            if numballs == 0:
                seriaPi.write("turn005l") 
                continue
            closestindex = 0
            i = 0
            while i < numballs:
                if abs(cx[i]-width/2) < abs(cx[closestindex]-width/2):
                    closestindex = 1
                i += 1
            bestcx, bestcy, bestr = cx[closestindex], cy[closestindex], r[closestindex]
            leverage = 10
            if width/2-leverage < bestcx < width/2+leverage:
                foundBall = True
                move = "left"
                amount = "180"
            elif bestcx < width/2:
                move = "right"
                amount = "005"
            elif bestcx > width/2:
                move = "left"
                amount = "005"
            if move == "forw":
                serialPi.write("move"+str(amount)+"f")
            elif move == "left":
                serialPi.write("turn"+str(amount)+"l")
            elif move == "right":
                serialPi.write("turn"+str(amount)+"r")
            continue
        
        else:
            inBallRoom = silverDetection.detectSilver()

        move = greenDetect.detectGreen(frame)
        if move != "skip":
            if move == "U":
                serialPi.write("turn180l")
            elif move == "left":
                serialPi.write("turn090l")
            elif move == "right":
                serialPi.write("turn090r")
            
        serialPi.write("cont")


main()

piCam.endprogram()

