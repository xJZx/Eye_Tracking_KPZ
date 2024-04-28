import cv2
import csv
import numpy as np
import pyautogui as pg


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

    # taking screenshot of the main screen to refer to its width and height, to create sectors
    screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)

    # sector precision factor
    s = 1

    # calculating number of sectors in x and y
    number_of_sectors_x = (screenshot.shape[:2][1] // (saved_coordinates[0][0] - saved_coordinates[2][0])) * s
    number_of_sectors_y = (screenshot.shape[:2][0] // (saved_coordinates[6][1] - saved_coordinates[0][1])) * s

    print("no. of x and y sectors", number_of_sectors_x, number_of_sectors_y)

    # calculating each sector width and height
    sector_width = screenshot.shape[:2][1] // number_of_sectors_x
    sector_height = screenshot.shape[:2][0] // number_of_sectors_y

    print("sector width and height", sector_width, sector_height)

    # creating the 2D array of sectors of type int, filled with zeros
    sectors = np.zeros((number_of_sectors_y, number_of_sectors_x), dtype=int)

    while True:
        screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)

        video, frame = cap.read()  # keep reading until we get a frame

        roi = frame[100:500, 100:500]

        rows, cols, _ = roi.shape

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

                # mirroring where the eye is looking
                x_middle = abs(x_middle - x2)
                y_middle = abs(y1 - y_middle)
            break

        # calculating the ratio for transposition of the eye focus
        s_x = int(screenshot.shape[:2][1]) / (saved_coordinates[0][0] - saved_coordinates[2][0])
        s_y = int(screenshot.shape[:2][0]) / (saved_coordinates[6][1] - saved_coordinates[0][1])
        # calculating new eye focus
        new_x = s_x * x_middle
        new_y = s_y * y_middle

        cv2.circle(screenshot, (int(new_x), int(new_y)), 5, (0, 0, 255), -1)

        # finding which sector to increment
        sector_x = int(new_x) // sector_width
        sector_y = int(new_y) // sector_height

        # incrementing the sector
        if sector_x <= number_of_sectors_x and sector_y <= number_of_sectors_y:
            sectors[sector_y][sector_x] += 1

        # print("xmid", x_middle)
        # print("ymid", y_middle)
        print("width", (saved_coordinates[0][0] - saved_coordinates[2][0]))
        print("height", (saved_coordinates[6][1] - saved_coordinates[0][1]))
        # print("sx", s_x)
        # print("sy", s_y)
        print("x", new_x)
        print("x i", int(new_x))
        print("y", new_y)
        print("y i", int(new_y))
        print("sector x", sector_x)
        print("sector y", sector_y)
        # print(sectors)

        cv2.imshow("threshold", threshold)
        cv2.imshow("gray frame", gray_frame)
        cv2.imshow("frame", frame)
        cv2.imshow("roi", roi)
        cv2.imshow('captured_screen', screenshot)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
