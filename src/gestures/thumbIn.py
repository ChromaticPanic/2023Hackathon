from gestures.gesture import Gesture 

from mediapipe import solutions as mp
import time

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
 
 
class ThumbIn(Gesture):
    DELAY = 1 # Used to prevent duplicate left click requests

    def check(self, handTracker) -> bool:
        # tip of thumb should be close to bottom of middle finger
        thumbX, thumbY = handTracker.readPointPosi(Points.THUMB_TIP)
        middleX, middleY = handTracker.readPointPosi(Points.MIDDLE_FINGER_MCP)

        # other fingers should not be bent
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        indexX, indexY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)
        ringX, ringY = handTracker.readPointPosi(Points.RING_FINGER_TIP)
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)
        
        thumbToMiddle = self.calcDist(thumbX, middleX, thumbY, middleY)
        wristToIndex = self.calcDist(wristX, indexX, wristY, indexY)
        wristToRing = self.calcDist(wristX, ringX, wristY, ringY)
        wristToPinky = self.calcDist(wristX, pinkyX, wristY, pinkyY)
        
        thumbToMiddle = self.normalize(thumbToMiddle, handTracker)
        wristToIndex = self.normalize(wristToIndex, handTracker)
        wristToRing = self.normalize(wristToRing, handTracker)
        wristToPinky = self.normalize(wristToPinky, handTracker)

        showing = False
        if thumbToMiddle and wristToIndex and wristToRing and wristToPinky:
            if thumbToMiddle <= 60 and wristToIndex >= 340 and wristToRing >= 325 and wristToPinky >= 300:
                showing = True

        return showing

    def triggerAction(self, handTracker, mouse):
        currAction = time.time()
        x, y = handTracker.readPointPosi()

        if currAction - self.lastAction >= ThumbIn.DELAY:
            print('Action: thumbsin')
            self.lastAction = currAction
            mouse.leftClick(int(x), int(y))
