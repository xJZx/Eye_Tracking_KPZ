import random

import numpy as np
import csv
import cv2
import pyautogui as pg


def make_screenshot():
    screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)
    return screenshot

def create_colored_heatmap_colormap(screenshot):
    sectors = []

    with open('sectors.csv', mode='r', newline='') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            sectors.append(row)

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

            # Normalizacja
            norm_value = int(sectors[y][x]) / max_sector_value
            
            # Pomijamy wartosci poniżej 0.02
            if norm_value < 0.02:
                continue

            # Szary pixel    
            gray_value = np.uint8(norm_value * 255)
            gray_image = np.full((1, 1), gray_value, dtype=np.uint8)

            # Aplikowanie COLORMAP_JET
            heatmap_color = cv2.applyColorMap(gray_image, cv2.COLORMAP_JET)[0][0]
            heatmap_color = np.full((sector_height, sector_width, 3), heatmap_color, dtype=np.uint8)

            # Blendujemy sektor z kolorem
            result = cv2.addWeighted(sector, 0.6, heatmap_color, 0.4, 0)

            screenshot[y * sector_height:(y * sector_height) + sector_height, x * sector_width:(x * sector_width) + sector_width] = result

    while True:
        cv2.imshow("Colored heatmap", screenshot)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break          


def create_heatmap(screenshot):
    sectors = []

    with open('sectors.csv', mode='r', newline='') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            sectors.append(row)

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


def create_gazeplots(screenshot):
    coordinates = []

    with open('circle_coordinates.csv', mode='r', newline='') as file_csv:
        reader = csv.reader(file_csv)
        for row in reader:
            coordinates.append(row)

    print(coordinates)

    screenshot = cv2.cvtColor(np.array(pg.screenshot()), cv2.COLOR_RGB2BGR)

    point_color = (0, 0, 255)  # Czerwony
    line_color = (0, 255, 0)  # Zielony
    thickness = 2

    first_point = True
    for point in coordinates:
        point[0] = float(point[0])
        point[1] = float(point[1])
        point[0] = int(point[0])
        point[1] = int(point[1])
        print(point)
        if first_point:
            cv2.circle(screenshot, tuple(point), 5, (255, 0, 0), -1)
            first_point = False
        else:
            cv2.circle(screenshot, tuple(point), 5, point_color, -1)

    # Narysuj linie między punktami
    for i in range(len(coordinates) - 1):
        start_point = coordinates[i]
        end_point = coordinates[i + 1]
        cv2.line(screenshot, start_point, end_point, line_color, thickness)

    while True:
        cv2.imshow("gazeplots", screenshot)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

