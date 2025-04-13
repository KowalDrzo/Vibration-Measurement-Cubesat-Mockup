from visualization import Visulization

import tkinter as tk
from tkinter import ttk
import serial
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

        self.bytes_amount = 0
        self.label_amount = tk.Label(self.root, text=f"Zapisano bajtów: {self.bytes_amount}.")
        self.label_amount.pack(pady=10)

        with open(self.filename, "w") as file:
            file.write(f"{self.scale}\n")

        self.ser = serial.Serial(self.port_name, 921600, timeout=1)
        self.thread = threading.Thread(target=self.read_serial_loop, daemon=True)
        self.thread.start()

        self.root.mainloop()

    def read_serial_loop(self):
        with open(self.filename, "a") as file:
            while self.running:
                data = self.ser.read(30000)
                if len(data) == 30000:
                    x = list(data[0:10000])
                    y = list(data[10000:20000])
                    z = list(data[20000:30000])

                    # Zapis do pliku
                    for xi, yi, zi in zip(x, y, z):
                        self.bytes_amount += file.write(f"{xi};{yi};{zi}\n")
                        self.label_amount.config(text=f"Zapisano bajtów: {self.bytes_amount}.")
                    file.flush()

            if self.ser.is_open:
                self.ser.close()
        return

    def stop_measurement(self):
        self.running = False
        time.sleep(0.1)
        self.root.destroy()  # zamknij okno pomiarów
        Visulization(self.filename)
