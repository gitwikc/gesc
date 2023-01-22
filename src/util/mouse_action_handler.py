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
        if ges_middle and not self.middle:
            self.middle = True
        if ges_right and not self.right:
            self.right = True

        if self.left:
            self.left = ges_left
        if self.middle:
            self.middle = ges_middle
        if self.right:
            self.right = ges_right

        if not self.mouse_lock:
            if self.left:
                pyautogui.mouseDown(button="left")
            if self.middle:
                pyautogui.mouseDown(button="middle")
            if self.right:
                pyautogui.mouseDown(button="right")

            if not ges_left and self.left:
                self.left = False
                pyautogui.mouseUp(button="left")
            elif not ges_middle and self.middle:
                self.middle = False
                pyautogui.mouseUp(button="middle")
            elif not ges_right and self.right:
                self.right = False
                pyautogui.mouseUp(button="right")

        else:
            # FIX Scroll continuously
            """
            Scroll down is -ve
            Scroll up is +ve
            """
            if self.left:
                pyautogui.scroll(-self.scroll_speed)
            elif self.right:
                pyautogui.scroll(self.scroll_speed)
            elif self.middle:
                exit(0)

    def toggle_mouse_lock(self):
        """
        Toggles the mouse lock
        """
        self.mouse_lock = not self.mouse_lock
