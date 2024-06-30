import cv2
import csv
import numpy as np
import pyautogui as pg
import math
import time
import video_heatmap

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def start_eye_tracking():
    chrome_options = Options()
    # chrome_options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome()

    # Open the website
    url = 'https://rekrutacja.pwr.edu.pl/'  # Replace with the website you want to open
    driver.get(url)

    page_height = driver.execute_script("return document.body.scrollHeight;")
    page_width = driver.execute_script("return document.body.scrollWidth;")

    cap = cv2.VideoCapture(0)

    # Check if the width and height were set successfully
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Resolution set to {}x{}".format(width, height))

    # recording
    screen_size = pg.size()
    rikord_widjo = cv2.VideoWriter('screen_recording.avi', cv2.VideoWriter_fourcc(*"XVID"), 10, (screen_size.width, screen_size.height))

    # Initialize the blank heatmap (black background)
    heatmap = np.zeros((screen_size[1], screen_size[0], 3), dtype=np.uint8)
    saved_coordinates = []

    time_counter = 0

    with open('circle_coordinates.csv', 'w') as file:  # delete data from file
        pass

    with open('calibration_coordinates.csv', mode='r', newline='') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            saved_coordinates.append([int(float(row[0])), int(float(row[1]))])

    print(saved_coordinates)

    # sector precision factor
    s = 1

    # calculating number of sectors in x and y
    number_of_sectors_x = (page_width // (saved_coordinates[0][0] - saved_coordinates[2][0])) * s
    number_of_sectors_y = (page_height // (saved_coordinates[6][1] - saved_coordinates[0][1])) * s

    print("no. of x and y sectors", number_of_sectors_x, number_of_sectors_y)

    # calculating each sector width and height
    sector_width = page_width // number_of_sectors_x
    sector_height = page_height // number_of_sectors_y

    print("sector width and height", sector_width, sector_height)

    # creating the 2D array of sectors of type int, filled with zeros
    sectors = np.zeros((number_of_sectors_y, number_of_sectors_x), dtype=int)

    while True:
        screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)

        video, frame = cap.read()  # keep reading until we get a frame

        roi = frame[0:500, 0:500]

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

        # eyeball diameter ~25mm
        eye_radius = 13

        non_linear_index = 0

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            x_middle = int(x + (w / 2))
            y_middle = int(y + (h / 2))
            # cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 3)
            if x1 < x_middle < x2 and y1 < y_middle < y2:
                cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
                cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)

                # as from trapezoid in paint
                # divide by 4 because pixel :(
                l = (math.sqrt((pow((x_middle - saved_coordinates[4][0]), 2) + (pow((y_middle - saved_coordinates[4][1]), 2))))) * 0.26458

                # mirroring where the eye is looking
                x_middle = abs(x_middle - x2)
                y_middle = abs(y1 - y_middle)

                if (eye_radius - l) >= 0:
                    x = math.sqrt((eye_radius ** 2) - (l ** 2))
                else:
                    x = eye_radius

                a = eye_radius - x

                s = math.sqrt((l ** 2) + (a ** 2))

                cosinus_alpha = 1 - (s ** 2 / (2 * (eye_radius ** 2)))
                if -1 < cosinus_alpha < 1:
                    alpha_rad = math.acos(cosinus_alpha)
                else:
                    break

                alpha = math.degrees(alpha_rad)

                arch = alpha / 360 * 2 * math.pi * eye_radius

                # try arch / l, because l is the path of an eye and we want to compare arch to this, not the s
                # l != 0 because if x and y middle are perfectly in the center of the pupil plane
                if l != 0:
                    non_linear_index = arch / l

                # print(l, x, a, s, cosinus_alpha, alpha, arch, non_linear_index)

            else:
                break
            break

        if non_linear_index != 0:
            # calculating the ratio for transposition of the eye focus
            s_x = int(screenshot.shape[:2][1]) / (saved_coordinates[0][0] - saved_coordinates[2][0])
            s_y = int(screenshot.shape[:2][0]) / (saved_coordinates[6][1] - saved_coordinates[0][1])
            # calculating new eye focus

            # half of the screen correct for non_linear_index
            if y_middle > saved_coordinates[4][1]:
                new_y = s_y * y_middle * non_linear_index
            else:
                # 2 - non_linear_index because in the upper half of the screen we want to lower the value, because number of pixel is growing from the upper-left corner
                new_y = s_y * y_middle * (2 - non_linear_index)

            if x_middle > saved_coordinates[4][0]:
                new_x = s_x * x_middle * non_linear_index
            else:
                new_x = s_x * x_middle * (2 - non_linear_index)

            if time.perf_counter() - time_counter > 1:
                with open('circle_coordinates.csv', mode='a', newline='') as file_csv:
                    writer = csv.writer(file_csv)
                    writer.writerow([new_x, new_y])
                time_counter = time.perf_counter()

            # finding which sector to increment
            scroll_y = int(driver.execute_script("return window.scrollY;"))
            sector_x = int(new_x) // sector_width
            sector_y = int(new_y) // sector_height + scroll_y // (page_height//number_of_sectors_y)
            # print(scroll_y)
            # print(scroll_y // 107)
            # print(new_y)
            # print(new_y // sector_height)
            # print(sector_x, sector_y)

            # incrementing the sector
            if sector_x < number_of_sectors_x and sector_y < number_of_sectors_y:
                sectors[sector_y][sector_x] += 1

            # generate video heatmap
            video_heatmap.create_heatmap(heatmap, screen_size[1], screen_size[0], int(new_x), int(new_y))
            screenshot = video_heatmap.apply_heatmap_to_frame_custom_intensity(heatmap, screenshot)

            # cool down the heatmap
            heatmap = video_heatmap.fade_heatmap(heatmap)

            cv2.circle(screenshot, (int(new_x), int(new_y)), 5, (0, 0, 255), -1)

        rikord_widjo.write(screenshot)

        # cv2.imshow("threshold", threshold)
        # cv2.imshow("gray frame", gray_frame)
        # cv2.imshow("frame", frame)
        cv2.imshow("roi", roi)
        cv2.imshow('captured_screen', screenshot)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    with open('sectors.csv', mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        for sector in sectors:
            writer.writerow(sector)

    cv2.destroyAllWindows()
