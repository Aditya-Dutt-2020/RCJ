import greenDetect
import ballDetect

import serialPi
import buttonStopper as bs
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

        if inBallRoom:
                cx,cy,r,silver = ballDetect.ballDetect(frame) #cx cy r and silver are all arrays that correspond with eachother. the silver array is true if its silver and false if its black
                #TODO calculate move and amount
                move=
                amount=
                

            if move != "skip":
                serialPi.write("stop")
                if move == "forw":
                    serialPi.write("move"+amount+"f")
                elif move == "left":
                    serialPi.write("turn"+amount+"l")
                elif move == "right":
                    serialPi.write("turn"+amount+"r")
                serialPi.write("cont")
            elif move == "skip": # there are no balls in vision
                serialPi.write("stop")
                seriaPi.write("turn001l")  #can also go right, or go more 
                serialPi.write("cont")

            continue
        
        else:
            inBallRoom = silverDetection.detectSilver()
            #TODO also serialwrite to tell the arduino to raise the camera up if inBallRoom is true


        move = greenDetect.detectGreen(frame)
        if move != "skip":
            serialPi.write("stop")
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

