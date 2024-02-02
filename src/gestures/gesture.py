from mediapipe import solutions as mp
from abc import ABC, abstractmethod
import math
 
Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class Gesture(ABC):
    CREATION_SCALE_LENGTH = 40

    def __init__(self):
        self.lastAction = 0

    def calcDist(self, x1, x2, y1, y2):
        dist = None

        if x1 and x2 and y1 and y2:
            dist = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

        return dist

    def normalize(self, dist, handTracker):
        scaledValue = None

        # normalizes the values (since hand to camera distance affects finger to finger distances)
        indexDipX, indexDipY = handTracker.readPointPosi(Points.INDEX_FINGER_DIP)
        indexTipX, indexTipY = handTracker.readPointPosi(Points.INDEX_FINGER_TIP)
        currLength = self.calcDist(indexDipX, indexTipX, indexDipY, indexTipY)

        if dist and currLength:
            scaledValue = dist*(Gesture.CREATION_SCALE_LENGTH/currLength)

        return scaledValue

    @abstractmethod
    def check(self, handTracker) -> bool:
        pass

    @abstractmethod
    def triggerAction(self, handTracker, mouse):
        pass
