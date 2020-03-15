import numpy as np
import cv2

cap = cv2.VideoCapture(0)


while 1:
    ret, frame = cap.read()
   
    w = int(frame.shape[1] * 0.2)
    h = int(frame.shape[0] * 0.2)
    dim = (w, h)
    
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA) 
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    new = frame.copy()
    for y in range(0, h):
        for x in range(0, w):
            p = new[y, x]
            if p > 120:
                new[y, x] = 0
    new = cv2.blur(new, (5, 5))
    mask = cv2.inRange(new, 70, 145)

    res = cv2.bitwise_and(frame,frame, mask= mask)
    ret, thresh = cv2.threshold(res, 67, 255, cv2.THRESH_BINARY)

    cv2.imshow("frame", frame)
    cv2.imshow("new", new)
    cv2.imshow("res", res)
    cv2.imshow("thres", thresh)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
