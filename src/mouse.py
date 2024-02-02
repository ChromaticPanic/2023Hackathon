from typing import Optional
import win32api, win32con, platform


class Mouse:
    def move(self, x: Optional[float], y: Optional[float]):
        if x and y:
            win32api.SetCursorPos((x, y))

    def leftClick(self, x: Optional[int], y: Optional[int]):
        if x and y:
            win32api.SetCursorPos((x, y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def rightClick(self, x: Optional[int], y: Optional[int]):
        if x and y:
            win32api.SetCursorPos((x, y))
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

    def detectOS(self):
        print(platform.system())