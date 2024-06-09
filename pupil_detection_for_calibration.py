import cv2
import csv
import keyboard
import time

def start_eye_tracking_calibration():
    saved_coordinates = []

    cap = cv2.VideoCapture(1)

    # Check if the width and height were set successfully
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Resolution set to {}x{}".format(width, height))

    is_space_pressed = False

    while True:
        video, frame = cap.read()  # keep reading until we get a frame

        roi = frame[100:500, 100:500]

        rows, cols, _ = roi.shape

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

            # if w > 5 and h > 5:
            x_middle = int(x + (w / 2))
            y_middle = int(y + (h / 2))
            # else:
            #     print("Eye not detected!")

            # cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 3)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(roi, (x_middle, y_middle), 2, (0, 0, 255), 10)
            cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
            cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
            break

        # cv2.imshow("threshold", threshold)
        # cv2.imshow("gray frame", gray_frame)
        # cv2.imshow("frame", frame)
        cv2.imshow("roi", roi)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        # elif key == ord(' '):
        if keyboard.is_pressed("space"):
            if x_middle != 0 and y_middle != 0 and not is_space_pressed:
                if len(saved_coordinates) < 9:
                    # added extra margin for error
                    if len(saved_coordinates) < 3:
                        saved_coordinates.append((x_middle, y_middle - 15))
                    elif len(saved_coordinates) > 5:
                        saved_coordinates.append((x_middle, y_middle + 15))
                    else:
                        saved_coordinates.append((x_middle, y_middle))
                else:
                    break
            is_space_pressed = True
            # time.sleep(0.2)  # Avoid high CPU usage
        else:
            is_space_pressed = False

    print(saved_coordinates)
    # saved_coordinates[0][0] += saved_coordinates[0][0] - 10
    # saved_coordinates[1][0] += saved_coordinates[1][0] - 10
    # saved_coordinates[2][0] += saved_coordinates[2][0] - 10
    #
    # saved_coordinates[6][0] += saved_coordinates[6][0] + 10
    # saved_coordinates[7][0] += saved_coordinates[7][0] + 10
    # saved_coordinates[8][0] += saved_coordinates[8][0] + 10
    with open('calibration_coordinates.csv', mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        for coordinate in saved_coordinates:
            writer.writerow(coordinate)
    cv2.destroyAllWindows()

