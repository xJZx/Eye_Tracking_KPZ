import threading

import pupil_detection
import pupil_detection_for_calibration
import calibration
import capture_the_screen

if __name__ == '__main__':
    t1 = threading.Thread(target=calibration.start_app)
    t2 = threading.Thread(target=pupil_detection_for_calibration.start_eye_tracking_calibration)
    t3 = threading.Thread(target=capture_the_screen.start_capture_the_screen)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


    pupil_detection.start_eye_tracking()
