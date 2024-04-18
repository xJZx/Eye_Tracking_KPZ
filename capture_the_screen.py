import cv2
import numpy as np
import pyautogui as pg


def start_capture_the_screen():
    while True:
        screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)
        cv2.imshow('captured_screen', screenshot)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
