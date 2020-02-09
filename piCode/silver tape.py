import sys
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

if (not cap.isOpened()):
    print("ERROR")
    exit()

while(cap.isOpened()):
    ret,frame=cap.read()
    if not ret:
        print("ret error")
        continue
    
    #frame=cv2.flip(frame,0)
    
    grayscaleframe=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscaleframe=cv2.GaussianBlur(grayscaleframe,(5,5),cv2.BORDER_DEFAULT)
    
    #_,bwframe=cv2.threshold(grayscaleframe,127,255,cv2.THRESH_BINARY)
    #_,bwframe=cv2.threshold(grayscaleframe,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    bwframe=cv2.adaptiveThreshold(grayscaleframe,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    
    
    cv2.imshow("bwframe before dialation",bwframe)
    
    kernel_dilation = np.ones((3,3), np.uint8)
    bwframe = cv2.dilate(bwframe, kernel_dilation, iterations=5)
    
    _, contours, h = cv2.findContours(bwframe,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    #cv2.drawContours(frame, contours,-1, (0,0,255), 3)
    
    silvertape=False
    for cnt in contours:
        cv2.drawContours(frame, [cnt],-1, (0,0,255), 3)
        if cv2.contourArea(cnt)>=1000:
            #ADD code to check if its actually the silver tape or just a black line
            silvertape=True
            break
    
    if silvertape:
        print("SILVER TAPE!!")
    if not silvertape:
        print("no silver tape")
    
        
    
    
    
    #print(len(contours))
    
    cv2.imshow("frame",frame)
    cv2.imshow("bwframe", bwframe)
    cv2.imshow("grayscaleframe", grayscaleframe)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


