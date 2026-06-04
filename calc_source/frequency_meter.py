import tkinter as tk
from tkinter import ttk

class FrequencyMeterConverter:
    def __init__(self, parent):
        self.parent = parent
        self.frequency_entry = None
        self.result_label = None
        self.convert_button = None
        self.converter_window = None
        self.meters_entry = None

    def open_frequency_converter(self):
        self.converter_window = tk.Toplevel(self.parent.root)
        self.converter_window.title("Frequency Meter Converter")
        self.converter_window.geometry("300x150")
        self.converter_window.transient(self.parent.root)
        self.converter_window.lift()  # Bring the window to the front
        self.converter_window.focus_force()  # Focus on the new window
        self.converter_window.bind("<Return>", lambda event: self.convert_frequency())  # Bind Enter key to convert
        self.converter_window.bind("<Escape>", lambda event: self.converter_window.destroy())  # Bind Escape key to close the window

        ttk.Label(self.converter_window, text="Frequency (MHz):").grid(row=0, column=0, padx=5, pady=5)
        self.frequency_entry = ttk.Entry(self.converter_window)
        self.frequency_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.converter_window, text="Or").grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(self.converter_window, text="Meters: ").grid(row=2, column=0, padx=5, pady=5)
        self.meters_entry = ttk.Entry(self.converter_window)
        self.meters_entry.grid(row=2, column=1, padx=5, pady=5)

        self.convert_button = ttk.Button(self.converter_window, text="Convert", command=self.convert_frequency)
        self.convert_button.grid(row=3, column=0, pady=5)

        self.result_label = ttk.Label(self.converter_window, text="")
        self.result_label.grid(row=3, column=1, pady=5)

    def convert_frequency(self):
        try:
            if self.frequency_entry.get() and self.meters_entry.get():
                tk.messagebox.showerror("Input Error", "Please enter a value for either frequency or wavelength, not both.")
            
            elif self.frequency_entry.get():
                frequency_mhz = float(self.frequency_entry.get())
                meters = 300 / frequency_mhz
                self.result_label.config(text=f"Wavelength: {meters:.2f} meters")

            elif self.meters_entry.get():
                meters = float(self.meters_entry.get())
                frequency_mhz = 300 / meters
                self.result_label.config(text=f"Frequency: {frequency_mhz:.2f} MHz")

            else:
                tk.messagebox.showerror("Input Error", "Please enter a value for either frequency or wavelength.")

        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter a valid number for frequency or wavelength.")
