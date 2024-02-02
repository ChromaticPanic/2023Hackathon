from gestures.gesture import Gesture

from mediapipe import solutions as mp
import time

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class L(Gesture):
    DELAY = 1 # used to prevent duplicate right click requests

    def check(self, handTracker) -> bool:
        # tip of thumb should be far from index
        thumbX, thumbY = handTracker.readPointPosi(Points.THUMB_TIP)
        indexX, indexY = handTracker.readPointPosi(Points.INDEX_FINGER_MCP)

        # other fingers should be bent
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        middleX, middleY = handTracker.readPointPosi(Points.MIDDLE_FINGER_TIP)
        ringX, ringY = handTracker.readPointPosi(Points.RING_FINGER_TIP)
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)
        
        thumbToIndex = self.calcDist(thumbX, indexX, thumbY, indexY)
        wristToMiddle = self.calcDist(wristX, middleX, wristY, middleY)    
        wristToRing = self.calcDist(wristX, ringX, wristY, ringY)
        wristToPinky = self.calcDist(wristX, pinkyX, wristY, pinkyY)
        
        thumbToIndex = self.normalize(thumbToIndex, handTracker)
        wristToMiddle = self.normalize(wristToMiddle, handTracker)
        wristToRing = self.normalize(wristToRing, handTracker)
        wristToPinky = self.normalize(wristToPinky, handTracker)

        showing = False
        if thumbToIndex and wristToMiddle and wristToRing and wristToPinky:
            if thumbToIndex >= 130 and wristToMiddle <= 110 and wristToRing <= 90 and wristToPinky <= 120:
                showing = True

        return showing

    def triggerAction(self, handTracker, mouse):
        currAction = time.time()
        x, y = handTracker.readPointPosi()

        if currAction - self.lastAction >= L.DELAY:
            print('Action: l')
            self.lastAction = currAction
            mouse.rightClick(int(x), int(y))
