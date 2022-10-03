from pprint import pprint
from time import sleep
from typing import List
import cv2
import mediapipe as mp
from collections import namedtuple
import numpy as np
import pandas as pd


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

HandSign = namedtuple('HandSign', ['id', 'name'])

# TODO Remove these later these are just test signs
fist = HandSign('FIST', 'Fist')
victory = HandSign('VICT', 'Victory')


def read_hands(signs: List[HandSign] = [], max_frames=200):
    sign_data = []
    with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        for sign in signs:
            print(f"Collecting data for '{sign.name}' in 5s...")
            sleep(5)
            frames_recorded = 0
            cap = cv2.VideoCapture(0)
            while cap.isOpened() and frames_recorded < max_frames:
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                        sign_data.append(np.array([
                            (point.x, point.y)
                            for point in hand_landmarks.landmark
                        ]).flatten().tolist())
                        frames_recorded += 1

                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
                cv2.waitKey(1)
            cap.release()
            cv2.destroyAllWindows()
    sign_data = np.array(sign_data)
    df = pd.DataFrame(data = sign_data)
    df['label'] = np.array([[sign.id] * max_frames for sign in signs])\
            .flatten().reshape(max_frames * len(signs), 1)
    df.to_csv('src/util/data_hand_signs/data/handsign.csv', index=False)


if __name__ == '__main__':
    read_hands([fist, victory])
