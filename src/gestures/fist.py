from gestures.gesture import Gesture

from mediapipe import solutions as mp
import time, win32gui, win32con

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)

 
class Fist(Gesture):
    DELAY = 1 # used to prevent duplicate close window requests

    def check(self, handTracker) -> bool:
        # thumb should be pressed to the index finger's knuckle
        thumbX, thumbY = handTracker.readPointPosi(Points.THUMB_TIP)
        indexPipX, indexPipY = handTracker.readPointPosi(Points.INDEX_FINGER_PIP)

        # pinky should be down
        pinkyX, pinkyY = handTracker.readPointPosi(Points.PINKY_TIP)
        
        # index and middle finger should be down
        wristX, wristY = handTracker.readPointPosi(Points.WRIST)
        indexTipX, indexTipY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)
        middleX, middleY = handTracker.readPointPosi(Points.MIDDLE_FINGER_TIP)
        ringX, ringY = handTracker.readPointPosi(Points.RING_FINGER_TIP)

        thumbToIndex = self.calcDist(thumbX, indexPipX, thumbY, indexPipY)
        wristToPinky = self.calcDist(wristX, pinkyX, wristY, pinkyY)
        wristToIndex = self.calcDist(wristX, indexTipX, wristY, indexTipY)
        wristToMiddle = self.calcDist(wristX, middleX, wristY, middleY)
        wristToRing = self.calcDist(wristX, ringX, wristY, ringY)

        thumbToIndex = self.normalize(thumbToIndex, handTracker)
        wristToPinky = self.normalize(wristToPinky, handTracker)
        wristToIndex = self.normalize(wristToIndex, handTracker)
        wristToMiddle = self.normalize(wristToMiddle, handTracker)
        wristToRing = self.normalize(wristToRing, handTracker)      

        showing = False
        if thumbToIndex and wristToPinky and wristToIndex and wristToMiddle and wristToRing:
            if thumbToIndex <= 35 and wristToPinky <= 100 and wristToIndex <= 125 and wristToMiddle <= 105 and wristToRing <= 90:
                showing = True

        return showing

    def triggerAction(self, handTracker, mouse):
        currAction = time.time()

        if currAction - self.lastAction >= Fist.DELAY:
            print('Action: fist')
            self.lastAction = currAction
            window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
