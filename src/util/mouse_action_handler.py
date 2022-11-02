import pyautogui


class MouseActionHandler:
    """
    Handles mouse actions like clicks and scrolling
    based on the current state of the handler
    """

    def __init__(self, scroll_speed: int) -> None:
        self.scroll_speed = scroll_speed
        self.left = self.right = self.middle = False
        self.mouse_lock = True
        # self.scrolling = False

    def update(self, ges_left: bool, ges_middle: bool, ges_right: bool):
        """
        Updates mouse action handler's state and performs the
        action corresponding the the change (click/scroll)
        """
        if ges_left and not self.left:
            self.left = True
            if not self.mouse_lock:
                pyautogui.mouseDown(button='left')
            else:
                pyautogui.scroll(-self.scroll_speed)
        elif ges_middle and not self.middle:
            self.middle = True
            if not self.mouse_lock:
                pyautogui.mouseDown(button='middle')
            else:
                pyautogui.scroll(self.scroll_speed)
        elif ges_right and not self.right:
            self.right = True
            if not self.mouse_lock:
                pyautogui.mouseDown(button='right')

        if not ges_left and self.left:
            self.left = False
            pyautogui.mouseUp(button='left')
        elif not ges_middle and self.middle:
            self.middle = False
            pyautogui.mouseUp(button='middle')
        elif not ges_right and self.right:
            self.right = False
            pyautogui.mouseUp(button='right')

    def toggle_mouse_lock(self):
        """
        Toggles the mouse lock
        """
        self.mouse_lock = not self.mouse_lock
