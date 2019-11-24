import cv2
import numpy as np
import sys

def findTrunc(image):
    width, height = image.shape[:2]
    #print("Total Pixels", width*height)    
    notBlack = cv2.countNonZero(image)
   # print("NonBlack", notBlack)
    if width*height == 0:
        print("Comes too close to border, move back")
        return 0
    Percentage = (notBlack / (width * height)) * 100
    #print("Percentage:", Percentage)
    return 1 if Percentage >= 70 else 0


def retSide(left, right):
    if left == 0 and right == 1:
        return 1
    if right == 0 and left == 1:
        return 0


def retTB(top, bottom):
    if top == 1 and bottom == 0:
        return 0
    if top == 0 and bottom == 1:
        return 1


def findBlack(xCoor, yCoor, wid, hei, size, image):
    ret, leftBox = cv2.threshold(image[yCoor:yCoor + hei, xCoor - size:xCoor], 120, 255, cv2.THRESH_BINARY)
    ret, rightBox = cv2.threshold(image[yCoor:yCoor + hei, xCoor + hei:xCoor + hei + size + 2], 120, 255, cv2.THRESH_BINARY)
    ret, topBox = cv2.threshold(image[yCoor - size:yCoor, xCoor:xCoor + hei], 120, 255, cv2.THRESH_BINARY)
    ret, bottomBox = cv2.threshold(image[yCoor + hei:yCoor + hei + 2 + size, xCoor:xCoor + hei], 120, 255, cv2.THRESH_BINARY)
    if leftBox is not None and rightBox is not None and topBox is not None and bottomBox is not None:
        cv2.imshow("Left", leftBox)
        cv2.imshow("Right", rightBox)
        cv2.imshow("Top", topBox)
        cv2.imshow("Bottom", bottomBox)
    else:
        print("Too close, move Back")
        return 0, 0, 0, 0
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.imwrite("Bottom.jpg", bottomBox)
        sys.exit()

    return findTrunc(leftBox), findTrunc(rightBox), findTrunc(topBox), findTrunc(bottomBox)


def getValues(theList, name):
    tup = ()
    for x in theList:
        tup = tup + (cv2.getTrackbarPos(x, name),)
    return tup


def nothing(x):
    pass

#bottomImage = cv2.imread("/home/pi/CV2/Green/Bottom.jpg")
#bottomImage = cv2.cvtColor(bottomImage, cv2.COLOR_BGR2GRAY)
#ret, bottomImage = cv2.threshold(bottomImage, 120, 255, cv2.THRESH_BINARY)
#cv2.imshow("bottom", bottomImage)
#cv2.waitKey()
#print("Bottom is", findTrunc(bottomImage))

cap = cv2.VideoCapture(0)


cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('HH', 'image', 174, 259, nothing)
cv2.createTrackbar('HS', 'image', 400, 255, nothing)
cv2.createTrackbar('HV', 'image', 230, 255, nothing)
cv2.createTrackbar('LH', 'image', 56, 259, nothing)
cv2.createTrackbar('LS', 'image', 92, 255, nothing)
cv2.createTrackbar('LV', 'image', 0, 255, nothing)





while cap.isOpened():
    ret, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgCopy = img.copy()
    imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_HSV2BGR)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    hh, hs, hv, lh, ls, lv = getValues(["HH", "HS", "HV", "LH", "LS", "LV"], 'image')
    lower = np.array([lh, ls, lv])
    higher = np.array([hh, hs, hv])
    mask = cv2.inRange(img, lower, higher)
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    newContours = []
    cv2.imshow('mask', mask)
    cv2.imshow('copy', imgCopy)
    for x in range(len(contours)):
        # print(cv2.contourArea(contours[x]))
        if cv2.contourArea(contours[x]) >= 500:
            newContours.append(contours[x])
    cv2.drawContours(imgCopy, newContours, -1, (255, 0, 0), 1)
    print(len(newContours))
    if len(newContours) == 0:
        print("No turn")
        continue
    elif len(newContours) == 1:
        x, y, w, h = cv2.boundingRect(newContours[0])
        # print(x, y, w, h)
        left, right, up, down = findBlack(x, y, w, h, 25, imgGray)
        print("Left is", left, "\tRight is", right, "\tTop is", up, "\tBottom is", down)
        if down == 0:
            print("Skip the turn")
            continue
        print("Left Turn" if right == 0 else "Right Turn")
        print("Doing This")
    # x, y gives bottom left corner coordinate

    elif len(newContours) == 2:
        contourDict = {}
        for z in range(len(newContours)):
            x, y, w, h = cv2.boundingRect(newContours[z])
            contourDict["Contour " + str(z)] = findBlack(x, y, w, h, 25, imgGray)
        # print(contourDict)
        # print(retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]))
        if retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) == 0 and retTB(contourDict["Contour 1"][2], contourDict["Contour 1"][3]) == 0:
            print("Skip")
            continue
        if retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) and retTB(contourDict["Contour 1"][2], contourDict["Contour 1"][3]):
            print("Double Green")
            continue
        if retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) == 0:
            print("Turn Left" if retSide(contourDict["Contour 1"][0], contourDict["Contour 1"][1]) == 0 else "Turn Right")
            continue
        else:
            print("Turn Left" if retSide(contourDict["Contour 0"][0], contourDict["Contour 0"][1]) == 0 else "Turn Right")

    elif len(newContours) == 3:
        contourDict = {}
        for z in range(len(newContours)):
            x, y, w, h = cv2.boundingRect(newContours[z])
            contourDict["Contour " + str(z)] = findBlack(x, y, w, h, 25, imgGray)
        if (
                retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) == 1 and retTB(contourDict["Contour 1"][2], contourDict["Contour 1"][3]) == 1 or
                retTB(contourDict["Contour 1"][2], contourDict["Contour 1"][3]) == 1 and retTB(contourDict["Contour 2"][2], contourDict["Contour 2"][3]) == 1 or
                retTB(contourDict["Contour 2"][2], contourDict["Contour 2"][3]) == 1 and retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) == 1
        ):
            print("U turn")
            continue
        if (retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) == 0 and
            retTB(contourDict["Contour 1"][2], contourDict["Contour 1"][3]) == 0
            ):
            print("Turn Left" if retSide(contourDict["Contour 2"][0], contourDict["Contour 2"][1]) == 0 else "Turn Right")
        if (retTB(contourDict["Contour 1"][2], contourDict["Contour 1"][3]) == 0 and
                retTB(contourDict["Contour 2"][2], contourDict["Contour 2"][3]) == 0
            ):
            print("Turn Left" if retSide(contourDict["Contour 0"][0], contourDict["Contour 0"][1]) == 0 else "Turn Right")
        if (retTB(contourDict["Contour 2"][2], contourDict["Contour 2"][3]) == 0 and
                retTB(contourDict["Contour 0"][2], contourDict["Contour 0"][3]) == 0
            ):
            print("Turn Left" if retSide(contourDict["Contour 1"][0], contourDict["Contour 1"][1]) == 0 else "Turn Right")
    elif len(newContours) == 4:
        print("U turn")

cap.release
cv2.destroyAllWindows()

