import cv2
import time
import math
import numpy as np
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from HandTrackingModule import HandDetector

wCam, hCam = 1280, 960
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
hmin, hmax = 50, 200
volBar, volPer, vol = 400, 0, 0
color = (0, 215, 255)

tipIds = [4, 8, 12, 16, 20]

mode = 'N'
active = 0

pyautogui.FAILSAFE = False

SMOOTHING_FACTOR = 0.5
prev_cursor_x, prev_cursor_y = 0, 0

left_click_active = False
right_click_active = False
_left_click_debounce_counter = 0
_right_click_debounce_counter = 0
DEBOUNCE_FRAMES = 3
CLICK_THRESHOLD_DISTANCE = 40

def putText(mode_text, loc=(30, 30), color=(0, 255, 255)):
    cv2.putText(img, str(mode_text), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, color, 2)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    prev_mode = mode
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        mode = 'Scroll'
        active = 1
    elif key == ord('v'):
        mode = 'Volume'
        active = 1
    elif key == ord('c'):
        mode = 'Cursor'
        active = 1
    elif key == ord('n'):
        mode = 'N'
        active = 0
    elif key == ord('q'):
        break

    if prev_mode == 'Cursor' and mode != 'Cursor':
        if left_click_active:
            pyautogui.mouseUp(button='left')
            left_click_active = False
            _left_click_debounce_counter = 0
        if right_click_active:
            pyautogui.mouseUp(button='right')
            right_click_active = False
            _right_click_debounce_counter = 0
    if key == ord('q'):
        if left_click_active:
            pyautogui.mouseUp(button='left')
            left_click_active = False
        if right_click_active:
            pyautogui.mouseUp(button='right')
            right_click_active = False

    fingers = []
    if len(lmList) != 0:
        if lmList[tipIds[0]][2] < lmList[tipIds[0] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

    if mode == 'Scroll' and active == 1 and len(lmList) != 0:
        putText('Scroll')
        if fingers[1] == 1 and fingers[2] == 1:
            x1, y1 = lmList[tipIds[1]][1], lmList[tipIds[1]][2]
            x2, y2 = lmList[tipIds[2]][1], lmList[tipIds[2]][2]
            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            if abs(y2 - y1) > 30:
                if y2 > y1:
                    putText('Scroll Down', loc=(30, 60), color=(0, 0, 255))
                    pyautogui.scroll(-200)
                else:
                    putText('Scroll Up', loc=(30, 60), color=(0, 255, 0))
                    pyautogui.scroll(200)
            else:
                putText('Scroll Ready', loc=(30, 60), color=(255, 255, 0))
        else:
            putText('Scroll (Inactive)', loc=(30, 60), color=(0, 100, 200))

    if mode == 'Volume' and active == 1 and len(lmList) != 0:
        putText('Volume')
        if fingers[0] == 1 and fingers[1] == 1:
            x1, y1 = lmList[tipIds[0]][1], lmList[tipIds[0]][2]
            x2, y2 = lmList[tipIds[1]][1], lmList[tipIds[1]][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)
            cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
            volBar = np.interp(vol, [minVol, maxVol], [400, 150])
            volPer = np.interp(vol, [minVol, maxVol], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            if length < 50:
                cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)
            cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
            cv2.rectangle(img, (30, int(volBar)), (55, 400), (215, 255, 127), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)
        else:
            putText('Volume (Inactive)', loc=(30, 60), color=(0, 100, 200))

    if mode == 'Cursor' and active == 1 and len(lmList) != 0:
        putText('Cursor')
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)
        if fingers[1] == 1:
            x1, y1 = lmList[tipIds[1]][1], lmList[tipIds[1]][2]
            screenWidth, screenHeight = pyautogui.size()
            X = int(np.interp(x1, [110, 620], [0, screenWidth - 1]))
            Y = int(np.interp(y1, [20, 350], [0, screenHeight - 1]))
            X = int(SMOOTHING_FACTOR * X + (1 - SMOOTHING_FACTOR) * prev_cursor_x)
            Y = int(SMOOTHING_FACTOR * Y + (1 - SMOOTHING_FACTOR) * prev_cursor_y)
            prev_cursor_x, prev_cursor_y = X, Y
            pyautogui.moveTo(X, Y)
            thumb_x, thumb_y = lmList[tipIds[0]][1], lmList[tipIds[0]][2]
            index_x, index_y = lmList[tipIds[1]][1], lmList[tipIds[1]][2]
            pinky_x, pinky_y = lmList[tipIds[4]][1], lmList[tipIds[4]][2]
            thumb_index_distance = math.hypot(thumb_x - index_x, thumb_y - index_y)
            thumb_pinky_distance = math.hypot(thumb_x - pinky_x, thumb_y - pinky_y)
            left_click_gesture_present = False
            if thumb_index_distance < CLICK_THRESHOLD_DISTANCE and fingers[0] == 1 and fingers[1] == 1:
                left_click_gesture_present = True
            if thumb_pinky_distance < CLICK_THRESHOLD_DISTANCE and fingers[0] == 1 and fingers[4] == 1:
                left_click_gesture_present = True
            if left_click_gesture_present:
                _left_click_debounce_counter = min(_left_click_debounce_counter + 1, DEBOUNCE_FRAMES)
                if _left_click_debounce_counter >= DEBOUNCE_FRAMES and not left_click_active:
                    pyautogui.mouseDown(button='left')
                    left_click_active = True
            else:
                _left_click_debounce_counter = max(_left_click_debounce_counter - 1, 0)
                if _left_click_debounce_counter == 0 and left_click_active:
                    pyautogui.mouseUp(button='left')
                    left_click_active = False
            middle_x, middle_y = lmList[tipIds[2]][1], lmList[tipIds[2]][2]
            thumb_middle_distance = math.hypot(thumb_x - middle_x, thumb_y - middle_y)
            right_click_gesture_present = False
            if thumb_middle_distance < CLICK_THRESHOLD_DISTANCE and fingers[0] == 1 and fingers[2] == 1:
                right_click_gesture_present = True
            if right_click_gesture_present:
                _right_click_debounce_counter = min(_right_click_debounce_counter + 1, DEBOUNCE_FRAMES)
                if _right_click_debounce_counter >= DEBOUNCE_FRAMES and not right_click_active:
                    pyautogui.mouseDown(button='right')
                    right_click_active = True
            else:
                _right_click_debounce_counter = max(_right_click_debounce_counter - 1, 0)
                if _right_click_debounce_counter == 0 and right_click_active:
                    pyautogui.mouseUp(button='right')
                    right_click_active = False
        else:
            putText('Cursor (Inactive)', loc=(30, 60), color=(0, 100, 200))
            if left_click_active:
                pyautogui.mouseUp(button='left')
                left_click_active = False
                _left_click_debounce_counter = 0
            if right_click_active:
                pyautogui.mouseUp(button='right')
                right_click_active = False
                _right_click_debounce_counter = 0

    if mode == 'N' or active == 0:
        putText('Neutral (Press s/v/c)', loc=(30, 60))

    cv2.imshow('Hand LiveFeed', img)

cap.release()
cv2.destroyAllWindows()
if left_click_active:
    pyautogui.mouseUp(button='left')
if right_click_active:
    pyautogui.mouseUp(button='right')
