import pyautogui


class MouseActionHandler:
    """
    Handles mouse actions like clicks and scrolling
    based on the current state of the handler
    """

    def __init__(self, scroll_speed: int) -> None:
        self.scroll_speed = scroll_speed
        self.left = self.right = self.middle = False
        self.moving = True
        self.scrolling = False

    def update(self, ges_left: bool, ges_middle: bool, ges_right: bool):
        """
        Updates mouse action handler's state and performs the
        action corresponding the the change (click/scroll)
        """
        if ges_left and not self.left:
            self.left = True
            if self.moving:
                pyautogui.mouseDown(button='left')
            else:
                pyautogui.scroll(-self.scroll_speed)
        elif ges_middle and not self.middle:
            self.middle = True
            if self.moving:
                pyautogui.mouseDown(button='middle')
            else:
                pyautogui.scroll(self.scroll_speed)
        elif ges_right and not self.right:
            self.right = True
            if self.moving:
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

    def toggle_mouse_mode(self):
        """
        Toggles the mouse mode between MOVE & SCROLL
        """
        self.moving = not self.moving
