import random

import numpy as np
import csv
import cv2
import pyautogui as pg


def create_heatmap():
    sectors = []

    with open('sectors.csv', mode='r', newline='') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            sectors.append(row)

    screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)

    sector_width = screenshot.shape[:2][1] // len(sectors[0])
    sector_height = screenshot.shape[:2][0] // len(sectors)

    max_sector_value = 0

    for y in range(len(sectors)):
        for x in range(len(sectors[0])):
            if int(sectors[y][x]) > max_sector_value:
                max_sector_value = int(sectors[y][x])

    for y in range(len(sectors)):
        for x in range(len(sectors[0])):
            sector = screenshot[y * sector_height:(y * sector_height) + sector_height, x * sector_width:(x * sector_width) + sector_width]
            rect = np.ones(sector.shape, dtype=np.uint8) * 255

            # rect = cv2.rectangle(screenshot, (x * sector_width, y * sector_height),
            #               ((x * sector_width) + sector_width, (y * sector_height) + sector_height), (0, 0, 0), -1)
            result = cv2.addWeighted(sector, 1 - int(sectors[y][x]) / max_sector_value, rect, int(sectors[y][x]) / max_sector_value, 0)

            screenshot[y * sector_height:(y * sector_height) + sector_height, x * sector_width:(x * sector_width) + sector_width] = result

    while True:
        cv2.imshow("heatmap", screenshot)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
