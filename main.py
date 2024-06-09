import threading

import heatmap
import pupil_detection
import pupil_detection_scroll
import pupil_detection_for_calibration
import calibration

if __name__ == '__main__':
    # t1 = threading.Thread(target=calibration.start_app)
    # t2 = threading.Thread(target=pupil_detection_for_calibration.start_eye_tracking_calibration)
    #
    # t1.start()
    # t2.start()
    #
    # t1.join()
    # t2.join()

    pupil_detection_scroll.start_eye_tracking()

    screenshot = heatmap.make_screenshot()
    heatmap.create_gazeplots(screenshot)
    heatmap.create_heatmap(screenshot)
    heatmap.create_colored_heatmap_colormap(screenshot)

