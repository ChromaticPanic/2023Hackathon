from gestures.setup import Setup
from gestures.thumbIn import ThumbIn
from gestures.l import L
from gestures.surfsUp import SurfsUp
from gestures.fist import Fist
from mouse import Mouse

from mediapipe import solutions as mp
from typing import Tuple, Optional
import numpy as np

import cv2, numpy.typing

Matlike = numpy.typing.NDArray[np.uint8]
Points = mp.hands.HandLandmark # 21 in total, well documented on [Google's developers website](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)


class HandTracker:
    def __init__(self, setupMode):
        self.input = mp.hands.Hands(max_num_hands=1)
        self.hand = None        # Hand loaded from a picture
        self.handPoints = []    # Referred to as landmarks, these are important points detected on a hand
           
        # List of gestures (checked in order), once one is detected, the others are aborted
        self.gestures = [  
            Setup(setupMode),   # Toggles setup mode (controlled by a constant in main)    
            ThumbIn(),
            L(),
            SurfsUp(),
            Fist()
        ]


    def loadHand(self, img: Matlike):
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB
        self.hand = self.input.process(imageRGB)        # Load the hand from the incomming picture

        self.handPoints.clear() # Ensures that all hand points are cleared to start for error checking

    def fingerFinder(self, img: Matlike):
        height, width = img.shape[:2] # We only need the first 2 values

        # If any points were detected, load them for the hand
        if self.hand.multi_hand_landmarks:
            currHand = self.hand.multi_hand_landmarks[0]

            # For each hand landmark, scale points by width and height, then save them
            for lm in currHand.landmark:
                x, y = int(lm.x * width), int(lm.y * height)
                self.handPoints.append([x, y])

    def draw(self, img: Matlike, window: str):
        x, y = self.readPointPosi()

        if self.hand.multi_hand_landmarks:
            currHand = self.hand.multi_hand_landmarks[0]
            mp.drawing_utils.draw_landmarks(img, currHand, mp.hands.HAND_CONNECTIONS)

        if x and y:
            cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

        cv2.imshow(window, img)

    def readGestures(self, mouse: Mouse):
        for gesture in self.gestures:
            showing = gesture.check(self)

            if showing:
                gesture.triggerAction(self, mouse)
                break

    def readPointPosi(self, handPoint: int=Points.INDEX_FINGER_TIP) -> Tuple[Optional[float], Optional[float]]:
        """
        Reads the X and Y coordinates of a given handPoint (default is the tip of index)
        If insufficient points are loaded, returns None
        """
        x, y = None, None

        if len(self.handPoints) > handPoint:
            x, y = self.handPoints[handPoint]

        return x, y
