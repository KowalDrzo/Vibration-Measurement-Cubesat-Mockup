import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
from datetime import datetime

class Measurement:
    def __init__(self, port, scale):
        self.port_name = port
        self.scale = scale
        self.root = tk.Tk()
        self.root.title("Pomiar")
        self.running = True

        self.filename = "Pomiar_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        ttk.Label(self.root, text=f"Zapis do pliku: {self.filename}").pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="STOP", command=self.stop_measurement)
        self.stop_button.pack(pady=5)

        # matplotlib wykres
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_title("Wykres czasowy")
        self.ax.set_xlabel("Próbka")
        self.ax.set_ylabel("Amplituda [skala ADC]")
        self.line1, = self.ax.plot([], [], label='X')
        self.line2, = self.ax.plot([], [], label='Y')
        self.line3, = self.ax.plot([], [], label='Z')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.ser = serial.Serial(self.port_name, 921600, timeout=1)
        self.thread = threading.Thread(target=self.read_serial_loop, daemon=True)
        self.thread.start()

        self.root.mainloop()

    def read_serial_loop(self):
        with open(self.filename, "a") as file:
            last_timestamp = 0
            while self.running:
                data = self.ser.read(30000)
                if len(data) == 30000:
                    x = list(data[0:10000])
                    y = list(data[10000:20000])
                    z = list(data[20000:30000])

                    # Zapis do pliku
                    for xi, yi, zi in zip(x, y, z):
                        file.write(f"{xi};{yi};{zi}\n")
                    file.flush()

                    # Odświeżenie wykresu
                    self.line1.set_data(range(len(x)), x)
                    self.line2.set_data(range(len(y)), y)
                    self.line3.set_data(range(len(z)), z)
                    self.ax.relim()
                    self.ax.autoscale_view()
                    self.canvas.draw_idle()

            if self.ser.is_open:
                self.ser.close()

    def stop_measurement(self):
        self.running = False
