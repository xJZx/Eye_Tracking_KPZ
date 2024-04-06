import cv2
import numpy as np


def start_eye_tracking():

    cap = cv2.VideoCapture(0)

    # Check if the width and height were set successfully
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Resolution set to {}x{}".format(width, height))


    while True:

        video = False  # wait for frame from USB device
        while video == False:
            video, frame = cap.read()  # keep reading until we get a frame

        rows, cols, _ = frame.shape
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)
        _, threshold = cv2.threshold(gray_frame, 3, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            #cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 3)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(frame, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
            cv2.line(frame, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
            break

        cv2.imshow("Threshold", threshold)
        cv2.imshow("gray frame", gray_frame)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()