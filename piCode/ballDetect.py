import sys
import numpy as np
import cv2

def ballDetect(frame)
    
    
    #frame=cv2.flip(frame,0)
    
    grayscaleframe=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print(grayscaleframe.shape)
    grayscaleframe=cv2.GaussianBlur(grayscaleframe,(5,5),cv2.BORDER_DEFAULT)
    
    #_,bwframe=cv2.threshold(grayscaleframe,127,255,cv2.THRESH_BINARY_INV)
    #_,bwframe=cv2.threshold(grayscaleframe,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    bwframe=cv2.adaptiveThreshold(grayscaleframe,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    '''
    _, contours, h = cv2.findContours(bwframe,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    indextoremove = []
    i=0
    while i<len(contours):
        if cv2.contourArea(contours[i])<=5:
            indextoremove.append(i)
        i=i+1
    contours = np.delete(contours,indextoremove)
    '''
    
    #cv2.imshow("bwframe before dialation",bwframe)
    
    kernel_dilation = np.ones((3,3), np.uint8)
    bwframe = cv2.dilate(bwframe, kernel_dilation, iterations=5)
    #print(bwframe.shape)
    _, contours, h = cv2.findContours(bwframe,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    '''
    indextoremove = []
    i=0
    while i<len(contours):
        if cv2.contourArea(contours[i])<=10:
            indextoremove.append(i)
        i=i+1
    contours = np.delete(contours,indextoremove)
    print(len(contours))
    #print(indextoremove)
    #print(contours)
    print(type(contours))
    
    
    if len(contours)>0 and contours is not None:
        cv2.drawContours(frame, contours,-1, (0,0,255), 3)
    '''
    
    xcoord=[]
    ycoord=[]
    radius=[]
    silver=[]
    
    for cnt in contours:
        cntarea=cv2.contourArea(cnt)
        if cntarea<=700:
            continue
        #see if its a circle
        
        #find inscribing circle{
        mask=np.zeros((480,640),np.uint8)
        cv2.drawContours(mask, [cnt],-1, (255), -1)
        #cv2.drawContours(frame, [cnt],-1, (0,0,255), 3)
        #_,mask=cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
        dist_transform=cv2.distanceTransform(mask,cv2.DIST_L2,5)
        argmax=dist_transform.argmax()
        #print(argmax)
        x=argmax%640
        y=int(argmax/640)
        r=dist_transform[y][x]
        #maxDT=np.unravel_index(argmax, dist_transform.shape)
        '''
        circlearea=r*r*3.14159
        if((cntarea-circlearea)>5000):
            continue
        '''
        #}
        
        _,R=cv2.minEnclosingCircle(cnt)
        if R-r>60:
            continue
        
        
        xcoord.append(x)
        ycoord.append(y)
        radius.append(r)
        
        
        mask2=np.zeros((480,640),np.uint8)
        cv2.circle(mask2, (x,y),r,255,-1)
        mean=cv2.mean(grayscaleframe,mask2)
        #print(mean)
        #cv2.imshow("mask2",mask2)
        #cv2.waitKey(0)
        if mean[0]>70: #white
            silver.append(True)
            #cv2.circle(frame, (x,y),r,(255,255,255),3)
        else:
            silver.append(False)
            #cv2.circle(frame, (x,y),r,(0,0,0),3)
        
    
    
    #print(len(contours))
    
    #cv2.imshow("frame",frame)
    
    #cv2.imshow("mask",mask)
    #cv2.imshow("bwframe", bwframe)
    #v2.imshow("grayscaleframe", grayscaleframe)
    
    
