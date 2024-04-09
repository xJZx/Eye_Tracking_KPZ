import tkinter as tk
import keyboard
import threading


class CalibrationApp:
    def __init__(self, master):
        self.master = master
        master.attributes("-fullscreen", True)
        master.configure(background='black')

        self.canvas = tk.Canvas(bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.radius = 10

        self.master.bind('<Key>', self.toggle_rendering)

        self.draw_calibration_points()

    def draw_calibration_points(self):
        circle_coords = [
            (0, 0),  # Top left corner
            (self.screen_width - self.radius * 2, 0),  # Top right corner
            (0, self.screen_height - self.radius * 2),  # Bottom left corner
            (self.screen_width - self.radius * 2, self.screen_height - self.radius * 2),  # Bottom right corner
            (self.screen_width / 2 - self.radius, 0),  # Middle of top edge
            (self.screen_width - self.radius * 2, self.screen_height / 2 - self.radius),  # Middle of right edge
            (0, self.screen_height / 2 - self.radius),  # Middle of left edge
            (self.screen_width / 2 - self.radius, self.screen_height - self.radius * 2),  # Middle of bottom edge
            (self.screen_width / 2 - self.radius, self.screen_height / 2 - self.radius)  # Middle of the screen
        ]

        # Create circles and store their object IDs
        for x, y in circle_coords:
            circle = self.canvas.create_oval(x, y, x + self.radius * 2, y + self.radius * 2, fill='red', outline='red')

    def draw_calibration(self):
        pass

    def toggle_rendering(self, event):
        pass


def start_app():
    root = tk.Tk()
    app = CalibrationApp(root)
    root.mainloop()
