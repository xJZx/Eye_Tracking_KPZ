import cv2
import numpy as np

# heatmap colors (blue to red spectrum)
# heatmap_colors = np.linspace(0, 255, 256, dtype=np.uint8)[:, np.newaxis]

# time (in seconds) after which the heatmap starts fading
fade_time = 10.0

# fading speed (amount to reduce intensity per second)
fade_speed = 255 / fade_time


def create_heatmap(heatmap, height, width, fixated_x, fixated_y, intensity=255, radius=25):
    y, x = np.ogrid[:height, :width]
    distance = np.sqrt((x - fixated_x)**2 + (y - fixated_y)**2)
    circular_mask = distance <= radius
    heatmap[circular_mask] = np.clip(heatmap[circular_mask] + intensity, 0, 255)


def fade_heatmap(heatmap):
    heatmap = np.maximum(heatmap - fade_speed, 0).astype(np.uint8)
    return heatmap


def apply_heatmap_to_frame(heatmap, frame):
    colored_heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_INFERNO)
    frame = cv2.addWeighted(frame, 1.0, colored_heatmap, 0.5, 0)
    return frame
