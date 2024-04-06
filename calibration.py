import tkinter as tk
import cv2
import numpy as np
import threading

class CalibrationApp:
    def __init__(self, master):
        self.master = master
        master.attributes("-fullscreen", True)
        master.configure(background='black')

        self.canvas = tk.Canvas(bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.draw_calibration_points()


    def draw_calibration_points(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        radius = 10

        # Top left corner
        self.canvas.create_oval(0, 0, radius * 2, radius * 2, fill='red', outline='red')
        # Top right corner
        self.canvas.create_oval(screen_width - radius * 2, 0, screen_width, radius * 2, fill='red', outline='red')
        # Bottom left corner
        self.canvas.create_oval(0, screen_height - radius * 2, radius * 2, screen_height, fill='red', outline='red')
        # Bottom right corner
        self.canvas.create_oval(screen_width - radius * 2, screen_height - radius * 2, screen_width, screen_height,
                                fill='red', outline='red')
        # Middle of top edge
        self.canvas.create_oval(screen_width / 2 - radius, 0, screen_width / 2 + radius, radius * 2, fill='red',
                                outline='red')
        # Middle of right edge
        self.canvas.create_oval(screen_width - radius * 2, screen_height / 2 - radius, screen_width,
                                screen_height / 2 + radius, fill='red', outline='red')
        # Middle of left edge
        self.canvas.create_oval(0, screen_height / 2 - radius, radius * 2, screen_height / 2 + radius, fill='red',
                                outline='red')
        # Middle of bottom edge
        self.canvas.create_oval(screen_width / 2 - radius, screen_height - radius * 2, screen_width / 2 + radius,
                                screen_height, fill='red', outline='red')
        # Middle of the screen
        self.canvas.create_oval(screen_width / 2 - radius, screen_height / 2 - radius, screen_width / 2 + radius,
                                screen_height / 2 + radius, fill='red', outline='red')


def start_app():
    root = tk.Tk()
    app = CalibrationApp(root)
    root.mainloop()

