import threading

import pupil_detection
import pupil_detection_for_calibration
import calibration

if __name__ == '__main__':
    t1 = threading.Thread(target=calibration.start_app)
    # t2 = threading.Thread(target=pupil_detection_for_calibration.start_eye_tracking_calibration)

    t1.start()
    # t2.start()

    t1.join()
    # t2.join()

    # pupil_detection.start_eye_tracking()
