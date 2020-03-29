import numpy as np
import cv2

def getRidBlack(img):
    img[np.where(img <= 60)] = 127
    return img

cap = cv2.VideoCapture(0)
silPic = cv2.imread("silvPic.png")
silPic = cv2.cvtColor(silPic, cv2.COLOR_BGR2GRAY)
silPic = np.rot90(silPic)
fac = 0.2
silPic = cv2.resize(silPic, (int(640*fac), int(480*fac)), interpolation = cv2.INTER_AREA) 

sub = cv2.createBackgroundSubtractorMOG2() 

while 1:
    ret, frame = cap.read()
    
    w = int(frame.shape[1] * fac)
    h = int(frame.shape[0] * fac)
    dim = (w, h)
    
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA) 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fbef = frame.copy()
    fbef = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    shad = sub.apply(frame)
    frame[np.where(shad==127)] += 15

    frame = getRidBlack(frame)

    s_frame = np.column_stack((frame, silPic))
    frame = cv2.equalizeHist(s_frame) 

    ret, thresh = cv2.threshold(frame, 225, 255, cv2.THRESH_BINARY)
#    ret, thresh1 = cv2.threshold(framefl, 225, 255, cv2.THRESH_BINARY)
#    thresh = cv2.bitwise_or(thresh, thresh1, mask=None)

    _, contours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)> 0:
        #print("E")
        contours.sort(key=cv2.contourArea)
        c = contours[-1]
        if cv2.contourArea(c) > 75:
            x,y,w,h = cv2.boundingRect(c)
            if x > 640:
                c = contours[-2]
                if cv2.contours(c) > 75:
                    x,y,w,h = cv2.boundingRect(c)
                    fbef = cv2.rectangle(fbef, (x, y), (x+w,y+w), (0,255,0),2) 
            else:
                fbef = cv2.rectangle(fbef,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("frame", frame)
    cv2.imshow("fbef", fbef)
    cv2.imshow("thres", thresh)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
