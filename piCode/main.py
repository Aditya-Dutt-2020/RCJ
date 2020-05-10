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

        frame = piCam.getFrame()

        serialPi.write("stop")

        if inBallRoom:
            ## Go to middle?

            if foundtr:
                grabbedBall = False
                serialPi.write("back005r")
                ## Turn camera/use other camera (if we use two)
                serialPi.write("turn180r")
                thresh = cv2.threshold(frame, 130, 255, cv2.THRESH_BINARY)
                if len(thresh[np.where(thresh==0)]) > frame.shape[0]*frame.shape[1]//2:
                    ## We are on the triangle
                    ## serialPi.write("open claw")
                    pass
                serialPi.write("turn180l")
                continue
            
            if grabbedBall:
                foundBall = False
                x, y, tr = detectTriangle(frame)
                if not tr:
                    serialPi.write("turn001l")
                else:
                    leverage = 10
                    if width/2-leverage < x < width/2+leverage:
                        serialPi.write("turn180r")
                        serialPi.write("back005r")
                        foundtr = True
                    elif x < width/2:
                        serialPi.write("turn005r")
                    elif x > width/2:
                        serialPi.write("turn005l")
                continue
                        
            if foundBall:
                serialPi.write("move05b")
                serialPi.write("Grab Ball Some How")
                serialPi.write("turn180r")
                cx,_,r,_ = ballDetect.ballDetect(frame)
                numballs = len(r)
                if numballs == 0:
                    grabbedBall = True
                    pass
                if numballs > 0:
                    grabBall = False
                    for x in cx:
                        leverage = 10
                        if width/2-leverage < x < width/2+leverage:
                            grabBall = True
                    if grabBall:
                        grabbedBall = True
                        pass
                if not grabbedBall:
                    serialPi.write("open claw some how cuz the ball isn't in it")
                continue
            
            cx,cy,r,silver = ballDetect.ballDetect(frame)
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

# Some how end program.
piCam.endprogram()

