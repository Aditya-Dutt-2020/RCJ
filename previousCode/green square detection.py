#import sys
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
    
    grayscaleframe=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _,blackandwhiteframe=cv2.threshold(grayscaleframe,127,255,cv2.THRESH_BINARY)
    
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    greensquare_hl=70
    greensquare_hh=101
    greensquare_sl=104
    greensquare_sh=255
    greensquare_vl=30
    greensquare_vh=120
    
    greensquare_hsvlow  = np.array([greensquare_hl, greensquare_sl, greensquare_vl])
    greensquare_hsvhigh = np.array([greensquare_hh, greensquare_sh, greensquare_vh])
    
    greensquare_mask = cv2.inRange(hsvframe, greensquare_hsvlow, greensquare_hsvhigh)
    _, contours, h = cv2.findContours(greensquare_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours,-1, (0,0,255), 3)
    
    '''
    print()
    print(len(contours))
    for cnt in contours:
        print(cv2.contourArea(cnt))
    cv2.waitKey(0);
    ''' #contour must have area > 10000
    
    
    #gs means green square
    gstopleft=False
    gstopright=False
    gsbottomleft=False
    gsbottomright=False
    numgreensquares=0
    wtf=False
    for cnt in contours:
        if cv2.contourArea(cnt)<7000:
            continue
        numgreensquares=numgreensquares+1
        print(cv2.contourArea(cnt))
        
        cntx,cnty,cntw,cnth = cv2.boundingRect(cnt)
        #centerx=cntx+cntw/2
        #centery=cnty+cnth/2
        
        #check if there is line to the top
        linetop=False
        x=cntx+cntw/2
        y=cnty -10
        x=int(x)
        y=int(y)
        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
            linetop=True
    
        #check if there is line to the bottom
        linebottom=False
        x=cntx+cntw/2
        y=cnty+cnth +10
        x=int(x)
        y=int(y)
        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
            linebottom=True
    
        #check if there is line to the left
        lineleft=False
        x=cntx -10
        y=cnty+cnth/2
        x=int(x)
        y=int(y)
        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
            lineleft=True
    
        #check if there is line to the right
        lineright=False
        x=cntx+cntw +10
        y=cnty+cnth/2
        x=int(x)
        y=int(y)
        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
            lineright=True
    
        
        if lineleft and lineright:
            wtf=True
        
        if lineright and linetop:
            gsbottomleft=True
        if lineleft and linetop:
            gsbottomright=True
        if lineright and linebottom:
            gstopleft=True
        if lineleft and linebottom:
            gstopright=True
        
        
    if wtf:
        print("wtf")
        
    elif gsbottomleft and gsbottomright:
        print("turn around")
        '''
        if numgreensquares >= 2:
            print("turn around")
        else:
            print("wtf")
        '''
    
    elif gsbottomleft:
        print("turn left")
    
    elif gsbottomright:
        print("turn right")
    
    else:
        print("do whatever")
    
    #maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)
    
    
    
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
