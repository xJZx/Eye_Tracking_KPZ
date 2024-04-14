import cv2
import numpy as np
import csv


def start_eye_tracking():

    cap = cv2.VideoCapture(0)

    # Check if the width and height were set successfully
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Resolution set to {}x{}".format(width, height))

    saved_coordinates = []

    with open('calibration_coordinates.csv', mode='r', newline='') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            saved_coordinates.append([int(float(row[0])), int(float(row[1]))])

    print(saved_coordinates)

    while True:

        # video = False  # wait for frame from USB device
        # while video == False:
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

        # (x1, y1), ((x1 + (x2 - x1), (y1 + (y2 - y1))        (x2 - x1) = width        (y2 - y1) = height
        (x1, y1) = saved_coordinates[2]  # bo lustrzane odbicie w kamerze
        (x2, y2) = saved_coordinates[6]  # bo lustrzane odbicie w kamerze
        # print(type(x2), type(x1))
        # print(x2, x1)
        cv2.rectangle(roi, (x2, y2), (x1, y1), (0, 0, 255), 2)

        x_middle = 0
        y_middle = 0

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            x_middle = int(x + (w / 2))
            y_middle = int(y + (h / 2))
            # cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 3)
            if x1 < x_middle < x2 and y1 < y_middle < y2:
                cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
                cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
            break

        cv2.imshow("threshold", threshold)
        cv2.imshow("gray frame", gray_frame)
        cv2.imshow("frame", frame)
        cv2.imshow("roi", roi)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
