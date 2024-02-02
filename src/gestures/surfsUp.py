from gestures.gesture import Gesture

from mediapipe import solutions as mp
import numpy as np
import os, cv2, time, pyautogui

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class SurfsUp(Gesture):
    DELAY = 1 # Used to prevent duplicate screen shot requests

    def check(self, handTracker) -> bool:
        # tip of thumb should be far from index
        thumbX, thumbY = handTracker.readPointPosi(Points.THUMB_TIP)
        indexMcpX, indexMcpY = handTracker.readPointPosi(Points.INDEX_FINGER_MCP)

        # other fingers should be bent
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        indexTipX, indexTipY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)
        middleX, middleY = handTracker.readPointPosi(Points.MIDDLE_FINGER_TIP)
        ringX, ringY = handTracker.readPointPosi(Points.RING_FINGER_TIP)
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)
        
        # Pinky should stick out
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)

        thumbToIndex = self.calcDist(thumbX, indexMcpX, thumbY, indexMcpY)
        wristToIndex = self.calcDist(wristX, indexTipX, wristY, indexTipY)
        wristToMiddle = self.calcDist(wristX, middleX, wristY, middleY)    
        wristToRing = self.calcDist(wristX, ringX, wristY, ringY)
        wristToPinky = self.calcDist(wristX, pinkyX, wristY, pinkyY)
        
        thumbToIndex = self.normalize(thumbToIndex, handTracker)
        wristToIndex = self.normalize(wristToIndex, handTracker)
        wristToMiddle = self.normalize(wristToMiddle, handTracker)
        wristToRing = self.normalize(wristToRing, handTracker)
        wristToPinky = self.normalize(wristToPinky, handTracker)

        indexDipX, indexDipY = handTracker.readPointPosi(Points.INDEX_FINGER_DIP)
        currLength = self.calcDist(indexDipX, indexTipX, indexDipY, indexTipY)

        showing = False
        if thumbToIndex and wristToIndex and wristToMiddle and wristToRing and wristToPinky:
            if thumbToIndex >= 150 and wristToIndex <= 225 and wristToMiddle <= 220 and wristToRing <= 215 and wristToPinky >= 355:
                showing = True

        return showing

    def triggerAction(self, handTracker, mouse):
        currAction = time.time()
        cwd = os.getcwd()
        os.chdir(cwd)

        if currAction - self.lastAction > SurfsUp.DELAY:
            print('Action: surfsup')
            self.lastAction = currAction

            img = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{currAction}.png', img)
