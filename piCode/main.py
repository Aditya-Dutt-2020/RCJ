import greenDetect
import ballDetect

import serialPi
import buttonStopper as bs
import piCam

import sys
import numpy as np
import cv2

import math


def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def main():
    serialPi.initSerial()
    bs.initButton()
    piCam.initialize()

    progStop = False
    inBallRoom = False

    brstate=0
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
        if inBallRoom: #need to add check if accidentally going out of the ball room
            cx,cy,r,silver = ballDetect.ballDetect(frame) #cx cy r and silver are all arrays that correspond with eachother. the silver array is true if its silver and false if its black
            numballs=len(r)
            if numballs==0:
                serialPi.write("t005l")
                brstate=0;
                sleeep(3)
                continue
            
            if(brstate==0):
                #find biggest one
                biggestindex=0
                i=0
                while i<numballs:
                    if r[i]>r[biggestindex]:
                        biggestindex=i
                    i+=1
                CX=cx[biggestindex]
                CY=cy[biggestindex]
                brstate=1
                continue
                
            
            if(brstate==1):
                if(r>99999):#change this later
                    #pick up ball and stuff
                    
                #lock on:
                #find point closest to CX,CY and make that the new CX,CY
                closestindex=0
                i=0
                while i<numballs:
                    if(dist(cx[i],cy[i],CX,CY)<dist(cx[closestindex],cy[closestindex],CX,CY)):
                        closestindex=i
                    i+=1
                CX=cx[closestindex]
                CY=cy[closestindex]
                #turn if necessary
                if CX>width/2-5 and CX<width/2+5:
                    #forward
                    serialPi.write("m002f")
                    
                elif CX<width/2:
                    #left
                    serialPi.write("t002l")
                    
                elif CX>width/2:
                    #right
                    serialPi.write("t002r")
            
                
            '''
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
            '''

            continue
        
        else:
            inBallRoom = silverDetection.detectSilver()
            #TODO also serialwrite to tell the arduino to raise the camera up if inBallRoom is true
            if inBallRoom:
                serialPi.write("idk what to put here")

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

