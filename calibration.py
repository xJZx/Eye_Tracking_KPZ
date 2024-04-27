import tkinter as tk
import keyboard
import threading
import time


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
        self.actual_circle = 0

        self.master.bind('<Key>', self.toggle_rendering)
        # self.listener_thread = threading.Thread(target=self.toggle_rendering)
        # self.listener_thread.start()

        self.circle_coords = [
            (0, 0),  # Top left corner
            (self.screen_width / 2 - self.radius, 0),  # Middle of top edge
            (self.screen_width - self.radius * 2, 0),  # Top right corner
            (0, self.screen_height / 2 - self.radius),  # Middle of left edge
            (self.screen_width / 2 - self.radius, self.screen_height / 2 - self.radius),  # Middle of the screen
            (self.screen_width - self.radius * 2, self.screen_height / 2 - self.radius),  # Middle of right edge
            (0, self.screen_height - self.radius * 2),  # Bottom left corner
            (self.screen_width / 2 - self.radius, self.screen_height - self.radius * 2),  # Middle of bottom edge
            (self.screen_width - self.radius * 2, self.screen_height - self.radius * 2)  # Bottom right corner
        ]

        self.draw_calibration_points()

    def draw_calibration_points(self):
        for x, y in self.circle_coords:
            if x == 0 and y == 0:
                self.canvas.create_oval(x, y, x + self.radius * 2, y + self.radius * 2, fill='green',
                                                 outline='green')
            else:
                self.canvas.create_oval(x, y, x + self.radius * 2, y + self.radius * 2, fill='red',
                                                 outline='red')

    def draw_calibration(self):
        i = 0
        for x, y in self.circle_coords:
            if i == self.actual_circle:
                self.canvas.create_oval(x, y, x + self.radius * 2, y + self.radius * 2, fill='green',
                                                 outline='green')
            else:
                self.canvas.create_oval(x, y, x + self.radius * 2, y + self.radius * 2, fill='red',
                                                 outline='red')
            i += 1

    def toggle_rendering(self, event):
        if event.keysym == 'space':
            if self.actual_circle < 8:
                self.actual_circle += 1
                self.draw_calibration()
            else:
                self.master.quit()

        # while True:
        #     if keyboard.is_pressed("space"):
        #         if self.actual_circle < 8:
        #             self.actual_circle += 1
        #             self.draw_calibration()
        #         else:
        #             self.master.quit()

            # time.sleep(0.1)  # Avoid high CPU usage


def start_app():
    root = tk.Tk()
    app = CalibrationApp(root)
    root.mainloop()
