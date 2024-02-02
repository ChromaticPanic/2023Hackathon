from gestures.gesture import Gesture

from mediapipe import solutions as mp

Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class Setup(Gesture):
    def __init__(self, inSetUp):
        self.inSetUp = inSetUp


    def check(self, handTracker) -> bool:
        return self.inSetUp

    def triggerAction(self, handTracker, mouse):
        """
        As per line 48, all future changes be calculated in a similar range i.e **[38 - 45]**
        Using this constraint, the calculated distances can be scaled to be used at multiple distances
        """
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
        
        # thumbToIndex = self.normalize(thumbToIndex, handTracker)
        # wristToIndex = self.normalize(wristToIndex, handTracker)
        # wristToMiddle = self.normalize(wristToMiddle, handTracker)
        # wristToRing = self.normalize(wristToRing, handTracker)
        # wristToPinky = self.normalize(wristToPinky, handTracker)

        indexTipX, indexTipY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)
        indexDipX, indexDipY = handTracker.readPointPosi(Points.INDEX_FINGER_DIP)
        currLength = self.calcDist(indexDipX, indexTipX, indexDipY, indexTipY)

        showing = False
        if thumbToMiddle and wristToIndex and wristToRing and wristToPinky:

            # The proximity used for all other gestures
            if currLength >= 38 and currLength <= 45:
               print(f'thumbToMiddle: {thumbToMiddle}, wristToIndex: {wristToIndex}, wristToRing: {wristToRing}, wristToPinky: {wristToPinky}') 
