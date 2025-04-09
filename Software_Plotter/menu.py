from measurement import Measurement

import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports

class Menu:

    VSA_CONSTANT = 0.304
    ADXL_CONSTANT = 0.647

    def __init__(self, root):
        self.root = root
        self.root.title("Menu pomiarowe")
        self.root.minsize(400, 300)  # Minimalny rozmiar

        self.scale_factor = tk.DoubleVar(value=1.0)
        self.serial_port = tk.StringVar()

        # Konfiguracja skalowania okna
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Frame główny
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=1)

        # Port szeregowy - etykieta i lista rozwijana
        ttk.Label(self.main_frame, text="Wybierz port szeregowy:").grid(row=0, column=0, columnspan=2, sticky="w")

        self.port_combo = ttk.Combobox(self.main_frame, textvariable=self.serial_port, state="readonly")
        self.port_combo.grid(row=1, column=0, sticky="ew")

        self.refresh_button = ttk.Button(self.main_frame, text="Odśwież", command=self.refresh_ports)
        self.refresh_button.grid(row=1, column=1, padx=5, sticky="ew")

        # RadioButtony do wyboru skali
        ttk.Label(self.main_frame, text="Wybierz czujnik:").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.scale_frame = ttk.Frame(self.main_frame)
        self.scale_frame.grid(row=3, column=0, columnspan=2, sticky="w")
        self.scale_factor = tk.DoubleVar(value=self.VSA_CONSTANT)
        ttk.Radiobutton(self.scale_frame, text="VSA004", variable=self.scale_factor, value=self.VSA_CONSTANT).pack(side="left", padx=5)
        ttk.Radiobutton(self.scale_frame, text="ADXL", variable=self.scale_factor, value=self.ADXL_CONSTANT).pack(side="left", padx=5)

        # Przycisk - nowy pomiar
        self.start_button = ttk.Button(self.main_frame, text="Zacznij nowy pomiar - zapis do pliku", command=self.start_new_measurement)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=(10, 5), sticky="ew")

        # Przycisk - wczytaj pomiar
        self.load_button = ttk.Button(self.main_frame, text="Wczytaj pomiar - wyświetl FFT", command=self.load_measurement)
        self.load_button.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

        self.refresh_ports()

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
        else:
            self.port_combo.set('')

    def start_new_measurement(self):
        selected_port = self.serial_port.get()
        scale = self.scale_factor.get()
        if not selected_port:
            messagebox.showerror("Błąd", "Wybierz port szeregowy.")
            return
        self.root.destroy()  # zamknij okno menu
        Measurement(selected_port, scale)  # otwórz nowe okno

    def load_measurement(self):
        messagebox.showinfo("Wczytywanie", "Tutaj w przyszłości będzie wczytywanie pomiarów z pliku")
