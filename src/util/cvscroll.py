from time import sleep

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from util.mouse_action_handler import MouseActionHandler


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def draw_circle_on_landmark(
    landmark, frame, frame_width, frame_height, radius, color, thickness
):
    cx, cy = 0, 0
    if type(landmark) == tuple:
        cx, cy = landmark
    else:
        cx, cy = landmark.x, landmark.y
    cv2.circle(
        frame,
        center=(int(cx * frame_width), int(cy * frame_height)),
        radius=radius,
        color=color,
        thickness=thickness,
    )


def distance(x1, y1, x2, y2) -> float:
    return np.linalg.norm((x2 - x1, y2 - y1))


def capture_video(scroll_speed=8, debug=False):
    capture = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()

    def fingers_touch(tip1, tip2, threshold=20) -> bool:
        return (
            distance(
                tip1.x * screen_width,
                tip1.y * screen_height,
                tip2.x * screen_width,
                tip2.y * screen_height,
            )
            < threshold
        )

    # The mouse action handler
    m_handler = MouseActionHandler(scroll_speed=scroll_speed)

    while capture.isOpened():
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_output = hand_detector.process(rgb_frame)
        hand_landmarks = hand_output.multi_hand_landmarks
        if hand_landmarks:
            # Plotting the hand connections
            for hand in hand_landmarks:
                # Calculate dynamic touch threshold
                touch_threshold = (
                    np.linalg.norm(
                        np.array(
                            [
                                (hand.landmark[5].x - hand.landmark[9].x) * frame_width,
                                (hand.landmark[5].y - hand.landmark[9].y)
                                * frame_height,
                            ]
                        )
                    )
                    * 2.2
                )

                if debug:
                    drawing_utils.draw_landmarks(
                        frame,
                        hand,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )
                index_tip, thumb_tip = hand.landmark[8], hand.landmark[4]
                if debug:
                    for fingertip_inx in [8, 4, 12, 16, 20]:
                        draw_circle_on_landmark(
                            hand.landmark[fingertip_inx],
                            frame,
                            frame_width,
                            frame_height,
                            radius=int(touch_threshold * 0.5),
                            color=(10, 200, 255),
                            thickness=4,
                        )

                # Move mouse
                if not m_handler.mouse_lock:
                    palm_borders = [hand.landmark[i] for i in [5, 9, 13, 17, 0]]
                    palm_center_mean_pos = np.mean(
                        [(base.x, base.y) for base in palm_borders], axis=0
                    )
                    mx, my = pyautogui.position()
                    stabz = 0.6
                    pyautogui.moveTo(
                        (
                            palm_center_mean_pos[0] * screen_width * (1 - stabz)
                            + mx * stabz
                        )
                        * 1.1,
                        (
                            palm_center_mean_pos[1] * screen_height * (1 - stabz)
                            + my * stabz
                        )
                        * 1.1,
                    )
                    if debug:
                        draw_circle_on_landmark(
                            (palm_center_mean_pos[0], palm_center_mean_pos[1]),
                            frame,
                            frame_width,
                            frame_height,
                            radius=10,
                            color=(230, 70, 20),
                            thickness=2,
                        )

                # Handle click gestures
                m_handler.update(
                    ges_left=fingers_touch(
                        thumb_tip, index_tip, threshold=touch_threshold
                    ),
                    ges_middle=fingers_touch(
                        thumb_tip, hand.landmark[12], threshold=touch_threshold
                    ),
                    ges_right=fingers_touch(
                        thumb_tip, hand.landmark[16], threshold=touch_threshold
                    ),
                )

                # Thumb + index == Lt-click
                if fingers_touch(thumb_tip, index_tip, threshold=touch_threshold):
                    if not m_handler.mouse_lock:
                        print("Left click!", index_tip.x, index_tip.y)
                        # pyautogui.click()
                        # pyautogui.sleep(1)
                    else:
                        # pyautogui.scroll(-scroll_speed)
                        pass
                # Thumb + ring == Rt-click
                if fingers_touch(
                    thumb_tip, hand.landmark[16], threshold=touch_threshold
                ):
                    if not m_handler.mouse_lock:
                        print("Right click!", index_tip.x, index_tip.y)
                        # pyautogui.click(button='right')
                        # pyautogui.sleep(1)
                    else:
                        # pyautogui.scroll(scroll_speed)
                        pass

                # Thumb + middle == middle click (toggle scrolling | ONLY in moving mode)
                if fingers_touch(
                    thumb_tip, hand.landmark[12], threshold=touch_threshold
                ):
                    if m_handler.mouse_lock:
                        print("EXIT")
                        capture.release()
                    elif not m_handler.mouse_lock:
                        # scrolling = True
                        # pyautogui.mouseDown(button='middle')
                        print("Scrolling now...")
                elif m_handler.mouse_lock:
                    pass
                    # scrolling = False
                    # pyautogui.mouseUp(button='middle')
                    # print('Scrolling end')

                    # Thumb + pinky == toggle mouse movement
                if fingers_touch(
                    thumb_tip, hand.landmark[20], threshold=touch_threshold
                ):
                    # moving = not moving
                    m_handler.toggle_mouse_lock()
                    print(
                        f"Mouse {'UNLOCKED' if not m_handler.mouse_lock else 'LOCKED'}"
                    )
                    sleep(0.5)
        if debug:
            cv2.imshow("Front Camera Feed", frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    # Before quitting press middle mouse because something happens to the taskbar
    pyautogui.click(button="middle")
