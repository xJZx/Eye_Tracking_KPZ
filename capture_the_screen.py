import cv2
import numpy as np
import pyautogui as pg


def start_capture_the_screen():
    screen_size = pg.size()
    video = cv2.VideoWriter('record.mp4', cv2.VideoWriter_fourcc(*"XVID"), 20, (screen_size.width, screen_size.height))

    while True:
        screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)
        cv2.imshow('captured_screen', screenshot)

        video.write(screenshot)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
