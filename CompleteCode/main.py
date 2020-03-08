#import GreenDetectTurn
#import ballDetect

import serialPi
#import buttonStopper as bs
#import piCam

import sys
import numpy as np
import cv2


#def main():
#    
##    bs.initButton()
##    piCam.initialize()
#
#    progStop = False
#    inBallRoom = False
#
#    while True:
#        if bs.getButton():
#            progStop = not progStop
#            if progStop == False:
#                serialPi.write("cont")
#            else:
#                serialPi.write("stop")
#        if progStop:
#            continue
#
#        frame = piCam.getFrame()
#
#        if inBallRoom: #have the arduino check if accidentally going out of the ball room
#            cx,cy,r,silver = ballDetect.ballDetect(frame) #cx cy r and silver are all arrays that correspond with eachother. the silver array is true if its silver and false if its black
#            numballs=len(r)
#            if numballs==0:
#                serialPi.write("turn020l")
#                #wait until complete
#                continue
#            #find one closest to middle
#            closestindex=0
#            i=0
#            while i<numballs:
#                if abs(cx[i]-width/2)<abs(cx[closestindex]-width/2):
#                    closestindex=i
#                i+=1
#            
#            if cx[closestindex]==width/2: #make it a range
#                
#            elif cx[closestindex]<width/2:
#                
#            elif cx[closestindex]>width/2:
#                
#            move=
#            amount=
#                
#
#            if move != "skip":
#                serialPi.write("stop")
#                if move == "forw":
#                    serialPi.write("move"+amount+"f")
#                elif move == "left":
#                    serialPi.write("turn"+amount+"l")
#                elif move == "right":
#                    serialPi.write("turn"+amount+"r")
#                serialPi.write("cont")
#            elif move == "skip": # there are no balls in vision
#                serialPi.write("stop")
#                seriaPi.write("turn001l")  #can also go right, or go more 
#                serialPi.write("cont")
#
#            continue
#        
#        else:
#            inBallRoom = silverDetection.detectSilver()
#            #TODO also serialwrite to tell the arduino to raise the camera up if inBallRoom is true
#            if inBallRoom:
#                serialPi.write("idk what to put here")

#move = greenDetect.detectGreen(frame)
#if move != "skip":
#    serialPi.write("stop")
#    if move == "U":
#        serialPi.write("turn180l")
#    elif move == "left":
#        serialPi.write("turn090l")
#    elif move == "right":
#        serialPi.write("turn090r")
#SerialPi.write("cont")
serialPi.initSerial()
while True:
    serialPi.write("cont")
    #print(serialPi.read())


#main()

# Some how end program.
#piCam.endprogram()

