from datetime import datetime
import cv2
import mediapipe as mp
from handTracker import handTracker
from mouseMover import mouseMove, mouseClick
import math

#input image or video
#identify if theres a person
#train model yolo, draws boxes around person
    
FRAMEWIDTH = 640
FRAMEHEIGHT = 480
MONITORWIDTH = 1920
MONITORHEIGHT = 1080
WINDOWNAME = "Video"
DEBOUNCETIME = 2
LASTCLICK = 0
CURRCLICK = 0

MA_WINDOW = 5  # Number of frames to include in moving average
ma_x, ma_y = [], []  # Lists to store cursor positions for moving average

# def scale to monitor size
def scaleToMonitor(xpos, ypos):
    x = xpos * MONITORWIDTH/FRAMEWIDTH
    y = ypos * MONITORHEIGHT/FRAMEHEIGHT
    return x,y

def main():
    #setting up the window properties
    cv2.namedWindow(WINDOWNAME,1)
    cv2.setWindowProperty(WINDOWNAME, cv2.WND_PROP_TOPMOST, 1)
    global LASTCLICK
    global CURRCLICK
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAMEWIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAMEHEIGHT)
    tracker = handTracker()

    while True:
        success,image = cap.read()
        if success:
            flippedImg = cv2.flip(image, 1)
            image = tracker.handsFinder(flippedImg)
            lmList = tracker.positionFinder(image)
            mpHands = tracker.getHandsModule()
            if len(lmList) != 0:
                #print(lmList[mpHands.HandLandmark.INDEX_FINGER_TIP])
                _,xpos,ypos = lmList[mpHands.HandLandmark.INDEX_FINGER_TIP]
                scaledX, scaledY = scaleToMonitor(xpos, ypos)

                ma_x.append(scaledX)
                ma_y.append(scaledY)

                # If moving average lists are longer than window size, remove oldest entry
                if len(ma_x) > MA_WINDOW:
                    ma_x.pop(0)
                    ma_y.pop(0)

                # Calculate moving average cursor position
                ma_x_avg = sum(ma_x) / len(ma_x)
                ma_y_avg = sum(ma_y) / len(ma_y)

                # Move cursor to smoothed position
                mouseMove(int(ma_x_avg), int(ma_y_avg))
                # mouseMove(int(scaledX), int(scaledY))

                _,x1,y1 = lmList[mpHands.HandLandmark.THUMB_TIP]
                _,x2,y2 = lmList[mpHands.HandLandmark.MIDDLE_FINGER_PIP]
                distance = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
                print(distance)
                if distance < 50:
                    CURRCLICK = datetime.now().second
                    #print("click")
                    if CURRCLICK - LASTCLICK > DEBOUNCETIME:
                        LASTCLICK = CURRCLICK
                        mouseClick(int(scaledX), int(scaledY))
                
            cv2.imshow(WINDOWNAME,image)    
            cv2.waitKey(1)

if __name__ == "__main__":
    main()

