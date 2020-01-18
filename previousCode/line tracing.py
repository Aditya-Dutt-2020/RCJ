import numpy as np
import cv2

cap = cv2.VideoCapture(0)

if (not cap.isOpened()):
    print("ERROR")
    exit()

'''
testimage = np.zeros((300,300,3), dtype="uint8")
testimage=cv2.cvtColor(testimage, cv2.COLOR_BGR2GRAY)
_,testimage=cv2.threshold(testimage,127,255,cv2.THRESH_BINARY)
'''

while(cap.isOpened()):
    ret,frame=cap.read()
    if not ret:
        print("ret error")
        continue
    imageheight,imagewidth,_=frame.shape
    
    frameoriginal=frame.copy()
    
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame=cv2.GaussianBlur(frame,(5,5),cv2.BORDER_DEFAULT)
    
    _,frame=cv2.threshold(frame,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    _, contours, h = cv2.findContours(frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    
    
    contourcolor = (0,0,255)
    #frame=cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    #print(contours, flush = True)
    if len(contours) == 0:
        print("abc")
        continue
    
    
    cnt= max(contours, key=cv2.contourArea)
    
    cv2.drawContours(frameoriginal, [cnt],-1, contourcolor, 3) #draw the biggest contour
    
    
    
    M = cv2.moments(cnt)
    if M['m00']==0:
        print("lol")
        continue
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(frameoriginal,(cx,cy),5,(255,0,0),5) #draw where the center is
    #moments is blue
    
    #x,y,w,h = cv2.boundingRect(cnt)
    #cv2.circle(frameoriginal,(int(x+w/2),int(y+h/2)),5,(0,255,0),5) #bounding rect is green
    
    
    if cx>imagewidth/2:
        veertext="veer right"
    elif cx<imagewidth/2:
        veertext="veer left"
    else:
        veertext="veer nowhere"
    
    cv2.putText(frameoriginal, veertext, (5, 20), 0, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    
    
    cv2.imshow("frame",frameoriginal)
    
   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()
