import cv2
import numpy as np
import csv


def start_eye_tracking_calibration():
    saved_coordinates = []

    top_left = (0, 0)
    top_middle = (0, 0)
    top_right = (0, 0)
    left_middle = (0, 0)
    middle = (0, 0)
    right_middle = (0, 0)
    bottom_left = (0, 0)
    bottom_middle = (0, 0)
    bottom_right = (0, 0)

    cap = cv2.VideoCapture(0)

    # Check if the width and height were set successfully
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Resolution set to {}x{}".format(width, height))


    while True:

        # video = False  # wait for frame from USB device
        # while not video:
        video, frame = cap.read()  # keep reading until we get a frame

        roi = frame[100:500, 100:500]

        rows, cols, _ = roi.shape
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)

        gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)
        _, threshold = cv2.threshold(gray_frame, 3, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        # (x, y) kordy lewego gornego punktu konturu
        # srodek: (x + (w / 2), y + (h / 2))

        x_middle = 0
        y_middle = 0

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w > 10 and h > 10:
                x_middle = int(x + (w / 2))
                y_middle = int(y + (h / 2))
                print("Eye not detected!")

            # cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 3)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(roi, (x_middle, y_middle), 2, (0, 0, 255), 10)
            cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
            cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
            break

        cv2.imshow("threshold", threshold)
        cv2.imshow("gray frame", gray_frame)
        cv2.imshow("frame", frame)
        cv2.imshow("roi", roi)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key == ord(' '):
            if x_middle != 0 and y_middle != 0:
                if len(saved_coordinates) < 8:
                    saved_coordinates.append((x_middle, y_middle))
                else:
                    saved_coordinates.append((x_middle, y_middle))
                    break

    print(saved_coordinates)
    with open('calibration_coordinates.csv', mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        for coordinate in saved_coordinates:
            writer.writerow(coordinate)
    cv2.destroyAllWindows()
