import tkinter as tk
from tkinter import messagebox, ttk

class WavelengthCalculator:
    def __init__(self, parent):
        self.parent = parent
        self.wavelength_window = None
        self.frequency_entry = None
        self.final_result = None
        self.calculate_button = None

    def open_wavelength_calculator(self):
        self.wavelength_window = tk.Toplevel(self.parent.root)
        self.wavelength_window.title("Wavelength Calculator")
        self.wavelength_window.geometry("300x150")
        self.wavelength_window.transient(self.parent.root)
        self.wavelength_window.lift()  # Bring the window to the front
        self.wavelength_window.focus_force()  # Focus on the new window
        self.wavelength_window.bind("<Return>", lambda event: self.calculate_button.invoke())  # Bind Enter key to calculate
        self.wavelength_window.bind("<Escape>", lambda event: self.wavelength_window.destroy())  # Bind Escape key to close the window

        # these sit side-by-side -------------
        tk.Label(self.wavelength_window, text="Frequency (MHz):").grid(row=0, column=0, padx=5, pady=5)
        self.frequency_entry = tk.Entry(self.wavelength_window)
        self.frequency_entry.grid(row=0, column=1, padx=5, pady=5)
        # ------------------------------------

        tk.Label(self.wavelength_window, text="(Wavelength = speed of light / Frequency)").grid(row=1, columnspan=2, pady=5)

        self.final_result = tk.StringVar()
        tk.Label(self.wavelength_window, textvariable=self. final_result, font=("Arial", 12)).grid(row=2, columnspan=2, pady=10)

        self.calculate_button = ttk.Button(self.wavelength_window, text="Calculate", command=self.calculate_wavelength)
        self.calculate_button.grid(row=3, columnspan=2, pady=10)

        self.wavelength_window.bind("<Return>", lambda event: self.calculate_button.invoke())  # Bind Enter key to calculate

    def calculate_wavelength(self):
        try:
            f = float(self.frequency_entry.get())
            if f <= 0:
                messagebox.showerror("Input Error", "Frequency must be greater than zero.")
                return
            c = 299792458  # speed of light in m/s
            wavelength = c / (f * 1e6)  # convert MHz to Hz
            self.final_result.set(f"Wavelength: {wavelength:.2f} meters")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")
