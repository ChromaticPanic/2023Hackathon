
from handTracker import HandTracker
from smoothMouse import SmoothMouse
import cv2

# If active, gestures are not detected and point distances are printed 
#    needs configruation in gestures/setup.py - triggerAction
SETUP_MODE = False

# Window Variables
WINDOW_NAME = 'Handler'
RESIZABLE = 1
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


def main():
    mouse = SmoothMouse(FRAME_WIDTH, FRAME_HEIGHT)
    tracker = HandTracker(SETUP_MODE)
    cap = initStream()

    # when hit 'q', terminate the program
    while cv2.waitKey(1) != ord('q'):
        success, img = cap.read()

        if success:
            img = cv2.flip(img, 1)
            
            tracker.loadHand(img)
            tracker.fingerFinder(img)
            tracker.readGestures(mouse)
            tracker.draw(img, WINDOW_NAME)

            x, y = tracker.readPointPosi()
            mouse.move(x, y)

    cap.release()


def initStream() -> cv2.VideoCapture:
    # setting up the window properties
    cv2.namedWindow(WINDOW_NAME, RESIZABLE)
    
    # Connects to default video device then sets up width and height for stream
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    return cap


if __name__ == "__main__":
    main()
