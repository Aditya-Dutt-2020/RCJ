import sys
import numpy as np
import cv2
import time
import serial

def initalize():
    cap = cv2.VideoCapture(0)

    if (not cap.isOpened()):
        print("ERROR")
        exit()




def getframe():
    while(cap.isOpened()):
        ret,frame=cap.read()
        if not ret:
            print("ret error")
            continue
        return frame
        
        
        
def endprogram():
    cap.release()
    cv2.destroyAllWindows()
    

