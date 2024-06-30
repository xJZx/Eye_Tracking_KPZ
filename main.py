import threading

import pupil_detection_enhanced
import static_heatmap
import pupil_detection
import pupil_detection_scroll
import pupil_detection_for_calibration
import calibration

if __name__ == '__main__':
    t1 = threading.Thread(target=calibration.start_app)
    t2 = threading.Thread(target=pupil_detection_for_calibration.start_eye_tracking_calibration)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    pupil_detection_enhanced.start_eye_tracking()
    # pupil_detection_scroll.start_eye_tracking()
    # pupil_detection.start_eye_tracking()

    # screenshot = static_heatmap.make_screenshot()
    # static_heatmap.create_gazeplots(screenshot)
    # static_heatmap.create_heatmap(screenshot)
    # static_heatmap.create_colored_heatmap_colormap(screenshot)

