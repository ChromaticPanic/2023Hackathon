from mouse import Mouse

from typing import Tuple, Optional

MOVE_AVG_WINDOW = 5  # Number of frames to include in moving average
MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080


class SmoothMouse(Mouse):
    def __init__(self, frameWidth: int, frameHeight: int):
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

        # Stores moved values to average (smooths out the mouse)
        self.moved_x = []
        self.moved_y = []

    
    def move(self, x: Optional[float], y: Optional[float]):
        if x and y:
            x, y = self._scaleToMonitor(x, y)
            move_avg_x, move_avg_y = self._getSmootherCursorPos(x, y)
            
            super().move(int(move_avg_x), int(move_avg_y))
    
    def leftClick(self, x: Optional[int], y: Optional[int]):
        if x and y:
            x, y = self._scaleToMonitor(x, y)
            super().leftClick(int(x), int(y))

    def rightClick(self, x: Optional[int], y: Optional[int]):
        if x and y:
            x, y = self._scaleToMonitor(x, y)
            super().rightClick(int(x), int(y))

    def _scaleToMonitor(self, x: float, y: float) -> Tuple[float, float]:
        x = x * MONITOR_WIDTH / self.frameWidth
        y = y * MONITOR_HEIGHT / self.frameHeight

        return x, y

    def _getSmootherCursorPos(self, x: float, y: float) -> Tuple[float, float]:
        self.moved_x.append(x)
        self.moved_y.append(y)

        # If moving average lists are longer than window size, remove oldest entry
        if len(self.moved_x) > MOVE_AVG_WINDOW:
            self.moved_x.pop(0)
            self.moved_y.pop(0)

        # Calculate moving average cursor position
        move_avg_x = sum(self.moved_x) / len(self.moved_x)
        move_avg_y = sum(self.moved_y) / len(self.moved_y)

        # return smoothed position
        return move_avg_x, move_avg_y
