import heatmap
import cv2

screenshot = cv2.imread("full_page_screenshot.png", cv2.IMREAD_COLOR)
heatmap.create_colored_heatmap_colormap(screenshot)