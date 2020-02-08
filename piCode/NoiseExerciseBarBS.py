import cv2
import numpy as np
import math
import time
cap = cv2.VideoCapture(0)
time.sleep(2)
def Enquiry(lis1):
    return(np.array(lis1))
def nothing(x):
    pass
cv2.namedWindow('circle')
cv2.createTrackbar('P2','circle',50,200,nothing)
cv2.createTrackbar('minDist','circle',100,2000,nothing)
cv2.createTrackbar('threshLow','circle',50,200,nothing)
switch = '0 : OFF \n1: ON;'
cv2.createTrackbar(switch, 'image',0,1,nothing)
while(cap.isOpened()):
#while(1):
    # Capture frame-by-frame
    ret, image = cap.read()
    if ret == False:
        print("False ret")
        break
    #image = cv2.imread('Blackball_resize.jpg')
    height, width = image.shape[:2]
    threshLow = cv2.getTrackbarPos('threshLow', 'circle')
    kernel = np.ones((5,5), np.uint8)
    image = cv2.resize(image, (math.floor(0.5*width),math.floor(0.5*height)), interpolation = cv2.INTER_CUBIC)
    #image = cv2.GaussianBlur(image,(5,5),0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, threshLow, 255, cv2.THRESH_BINARY_INV)
    rows = thresh.shape[0]
 #   while(1):
    md = cv2.getTrackbarPos('minDist', 'circle')
    p2 = cv2.getTrackbarPos('P2','circle')
    s = cv2.getTrackbarPos(switch, 'circle')
    #print(maxRad)
    image_cpy = image.copy()
    cv2.imshow("image", thresh)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    if s == 0:
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT,1, minDist = 100, param1=1529 , param2=12, minRadius = 20, maxRadius = 40)
    else:
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT,2, minDist = md, param1 = 50, param2=p2, minRadius = 0, maxRadius = 0)
    if circles is None:
        print ("No Circle")
    if circles is not None:
        #Round the coordinates and radius
        circles = np.round(circles[0, :]).astype("int")
        for (x,y,r) in circles:
            #output is in x,y,r(coordinates, radius) 
            radius = r
            center = (x,y)
            cv2.rectangle(image_cpy, (x-1, y-1), (x+1, y+1), (0,128,255), -1)
            cv2.line(image_cpy, center, (x+r,y), (0,255,0), 1)
            cv2.circle(image_cpy,center,r,(255,0,0),1)
            cropped = thresh[y-r:y+r, x-r:x+r]
            cv2.imwrite("thresh.jpg", thresh)
            #print("x, y, r is: ", x, y, r)
            #print(cropped)
            if Enquiry(cropped).size:
                cv2.imshow('cropped', cropped)
                white = cv2.countNonZero(cropped)
                percentage = (white/cropped.size)*100
                if percentage > 60:
                    print("This is a black ball")
                else:
                    print("This is a silver ball")
            #cv2.waitKey()
        #print(len(circles))
    # Display the resulting frame
    cv2.imshow('Camera1',image_cpy)
    #cv2.imshow('camera2', thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
  #  if cropped is not None:
        break

#cap.release()
cv2.destroyAllWindows()
