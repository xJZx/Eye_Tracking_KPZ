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

    def draw_calibration_points(self):


        # Top left corner
        self.canvas.create_oval(0, 0, self.radius * 2, self.radius * 2, fill='red', outline='red')
        # Top right corner
        self.canvas.create_oval(self.screen_width - self.radius * 2, 0, self.screen_width, self.radius * 2, fill='red', outline='red')
        # Bottom left corner
        self.canvas.create_oval(0, self.screen_height - self.radius * 2, self.radius * 2, self.screen_height, fill='red', outline='red')
        # Bottom right corner
        self.canvas.create_oval(self.screen_width - self.radius * 2, self.screen_height - self.radius * 2, self.screen_width, self.screen_height,
                                fill='red', outline='red')
        # Middle of top edge
        self.canvas.create_oval(self.screen_width / 2 - self.radius, 0, self.screen_width / 2 + self.radius, self.radius * 2, fill='red',
                                outline='red')
        # Middle of right edge
        self.canvas.create_oval(self.screen_width - self.radius * 2, self.screen_height / 2 - self.radius, self.screen_width,
                                self.screen_height / 2 + self.radius, fill='red', outline='red')
        # Middle of left edge
        self.canvas.create_oval(0, self.screen_height / 2 - self.radius, self.radius * 2, self.screen_height / 2 + self.radius, fill='red',
                                outline='red')
        # Middle of bottom edge
        self.canvas.create_oval(self.screen_width / 2 - self.radius, self.screen_height - self.radius * 2, self.screen_width / 2 + self.radius,
                                self.screen_height, fill='red', outline='red')
        # Middle of the screen
        self.canvas.create_oval(self.screen_width / 2 - self.radius, self.screen_height / 2 - self.radius, self.screen_width / 2 + self.radius,
                                self.screen_height / 2 + self.radius, fill='red', outline='red')

    def draw_calibration(self):

        amount_of_coords_saved = 0

        while amount_of_coords_saved < 8:
            match amount_of_coords_saved:
                case 0:
                    self.canvas.create_oval(0, 0, self.radius * 2, self.radius * 2, fill='green', outline='green')
                case 1:
                    self.canvas.create_oval(self.screen_width - self.radius * 2, 0, self.screen_width, self.radius * 2, fill='green', outline='green')
                case 2:
                    self.canvas.create_oval(0, self.screen_height - self.radius * 2, self.radius * 2, self.screen_height, fill='green', outline='green')
                case 3:
                    self.canvas.create_oval(self.screen_width - self.radius * 2, self.screen_height - self.radius * 2, self.screen_width, self.screen_height,
                                    fill='green', outline='green')
                case 4:
                    self.canvas.create_oval(self.screen_width / 2 - self.radius, 0, self.screen_width / 2 + self.radius, self.radius * 2, fill='green',
                                    outline='green')
                case 5:
                    self.canvas.create_oval(self.screen_width - self.radius * 2, self.screen_height / 2 - self.radius, self.screen_width,
                                    self.screen_height / 2 + self.radius, fill='green', outline='green')
                case 6:
                    self.canvas.create_oval(0, self.screen_height / 2 - self.radius, self.radius * 2, self.screen_height / 2 + self.radius, fill='green',
                                    outline='green')
                case 7:
                    self.canvas.create_oval(self.screen_width / 2 - self.radius, self.screen_height - self.radius * 2, self.screen_width / 2 + self.radius,
                                    self.screen_height, fill='green', outline='green')
                case 8:
                    self.canvas.create_oval(self.screen_width / 2 - self.radius, self.screen_height / 2 - self.radius, self.screen_width / 2 + self.radius,
                                    self.screen_height / 2 + self.radius, fill='green', outline='green')

            if keyboard.is_pressed('space'):
                amount_of_coords_saved += 1


def start_app():
    root = tk.Tk()
    app = CalibrationApp(root)
    thread1 = threading.Thread(target=app.draw_calibration_points)
    thread2 = threading.Thread(target=app.draw_calibration)
    thread1.start()
    thread2.start()
    root.mainloop()
    thread1.join()
    thread2.join()

