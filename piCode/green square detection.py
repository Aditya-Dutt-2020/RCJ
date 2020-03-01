#import sys
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
DIM=(640, 480)
K=np.array([[311.51864191859397, 0.0, 312.88731000462695], [0.0, 311.639944935319, 236.31857286816083], [0.0, 0.0, 1.0]])
D=np.array([[-0.04571824163435292], [0.015038557310671058], [-0.001927839108240956], [-0.01107170271825315]])
def undistort(theImg):
    img = theImg
    balance=0
    dim2 = (475, 356)
    dim3=None
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img
if (not cap.isOpened()):
    print("ERROR")
    exit()

while(cap.isOpened()):
    ret,frame=cap.read()
    frame = undistort(frame)
    imgHeight = frame.shape[0]
    imgWidth = frame.shape[1]
    if not ret:
        print("ret error")
        continue
    
    grayscaleframe=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _,blackandwhiteframe=cv2.threshold(grayscaleframe,200,255,cv2.THRESH_BINARY)
    
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    greensquare_hl=61
    greensquare_hh=91
    greensquare_sl=197
    greensquare_sh=400
    greensquare_vl=71
    greensquare_vh=220
    
    greensquare_hsvlow  = np.array([greensquare_hl, greensquare_sl, greensquare_vl])
    greensquare_hsvhigh = np.array([greensquare_hh, greensquare_sh, greensquare_vh])
    
    greensquare_mask = cv2.inRange(hsvframe, greensquare_hsvlow, greensquare_hsvhigh)
    contours, h = cv2.findContours(greensquare_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours,-1, (0,0,255), 3)
    
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
    frameCopy = frame.copy()
    for cnt in contours:
        if cv2.contourArea(cnt)<20000:
            continue
        cv2.drawContours(frameCopy, cnt,-1, (0,0,255), 3)
        numgreensquares+=1
        #print(cv2.contourArea(cnt))
        
        cntx,cnty,cntw,cnth = cv2.boundingRect(cnt)
       # print(cntw*cnth)
        if (cntw*cnth) > 94000:
            continue
       # print("Area of bounding box is: ", cntw*cnth)
      #  cv2.rectangle(frameCopy, (cntx, cnty), (cntx+cntw, cnty+cnth), (0, 255, 0), 3)
        cv2.rectangle(frameCopy, (cntx, cnty-40), (cntx+cntw, cnty-20), (255, 255, 0), 3)
        cv2.rectangle(frameCopy, (cntx, cnty+cnth+20), (cntx+cntw, cnty+cnth+40), (255, 255, 0), 3)
        cv2.rectangle(frameCopy, (cntx-40, cnty), (cntx, cnty+cnth), (255, 255, 0), 3)
      #  cv2.rectangle(frameCopy, (cntx+cntw, cnty), (cntx+cntw+40, cnty+cnth), (255, 255, 0), 3)
        #centerx=cntx+cntw/2
        #centery=cnty+cnth/2
        linetop = False
        linebottom = False
        lineright = False
        lineleft = False
        numWhite = 0
        
        if(cnty-40 >= 0 and cntx+cntw <= imgWidth):
           # print(cnty, cntx, cntw)
            totalPix = 20*cntw + 1
            roiT = blackandwhiteframe[(cnty-40):cnty-20, cntx:(cntx+cntw)]
            numWhite = cv2.countNonZero(roiT)
           # print("Left: ", numWhite/totalPix, end="", flush=True)
            if (numWhite / totalPix) < .25:
                linetop = True
#            cv2.imshow("roit", roiT)
        if(cnty+cnth+40 <= imgHeight and cntx+cntw <= imgWidth):
            totalPix = 20*cntw + 1
            roiB = blackandwhiteframe[(cnty +cnth+20):(cnty+cnth+40), cntx:(cntx+cntw)]
            numWhite = cv2.countNonZero(roiB)
            #print("\tBottom: ", numWhite/totalPix, end="", flush=True)
            #print("Left: ", numWhite, "\t", totalPix, "\t", numWhite/totalPix)
            if (numWhite / totalPix) < .25:
                linebottom = True
#            cv2.imshow("roib", roiB)
        if(cntx-40 >= 0 and cnty+cnth <= imgHeight):
            totalPix = cnth*40 + 1
            roiL = blackandwhiteframe[(cnty):(cnty+cnth), (cntx-40):(cntx)]
            numWhite = cv2.countNonZero(roiL)

            if (numWhite / totalPix) < .25:
                lineleft = True            
#            cv2.imshow("roil", roiL)
        if(cntx+cntw+40 <= imgWidth and cnty+cnth <= imgWidth):
            totalPix = cnty*20 + 1
            roiR = blackandwhiteframe[cnty:(cntx+cntw), (cntx+cntw+20):(cntx+cntw+40)]
            numWhite = cv2.countNonZero(roiR)
            #print("\tRight: ", numWhite/totalPix)
            if (numWhite / totalPix) < .25:
                lineright = True            
 #           cv2.imshow("roir", roiR)
        #check if there is line to the top
#        linetop=False
#        x=cntx+cntw/2
#        y=cnty -10
#        x=int(x)
#        y=int(y)
#        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
#            linetop=True
#    
#        #check if there is line to the bottom
#        linebottom=False
#        x=cntx+cntw/2
#        y=cnty+cnth +10
#        x=int(x)
#        y=int(y)
#        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
#            linebottom=True
#    
#        #check if there is line to the left
#        lineleft=False
#        x=cntx -10
#        y=cnty+cnth/2
#        x=int(x)
#        y=int(y)
#        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
#            lineleft=True
#    
#        #check if there is line to the right
#        lineright=False
#        x=cntx+cntw +10
#        y=cnty+cnth/2
#        x=int(x)
#        y=int(y)
#        if y<len(blackandwhiteframe) and x<len(blackandwhiteframe[0]) and x>=0 and y>=0 and blackandwhiteframe[y][x] == 0:
#            lineright=True
#    
        
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
        #print("Line Left: ", lineleft, "\tLine Right: ", lineright, "\tLine Top: ", linetop, "\tLine Bottom", linebottom)
        
  #  cv2.imshow("frame",frameCopy)
  #  cv2.imshow("mask", greensquare_mask)
    
 #   cv2.imshow("grayscale", blackandwhiteframe)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
      
    if wtf:
        print("wtf")
        
    elif gsbottomleft and gsbottomright:
        print("turn around")


        if numgreensquares >= 2:
            print("turn around")
        else:
            print("wtf")
        
   
    elif gsbottomleft:
       print("turn left")
    
    elif gsbottomright:
       print("turn right")
    
    else:
       print("do whatever")
    
    #maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)

    
    


cap.release()
cv2.destroyAllWindows()
