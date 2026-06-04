from tkinter import ttk
import tkinter as tk
from calc_source.ohms_law import OhmsLawCalculator
from calc_source.wavelength import WavelengthCalculator

class Calculators:
    def __init__(self, parent):
        self.parent = parent

        self.wavelength_window = None
        self.frequency_entry = None
        self.final_result = None
        self.calculate_button = None

        self.calc_window = tk.Toplevel(self.parent.root)
        self.calc_window.title("Calculators")
        self.calc_window.geometry("300x200")
        self.calc_window.transient(self.parent.root)
        self.calc_window.lift()  # Bring the window to the front
        self.calc_window.bind("<Escape>", lambda event: self.calc_window.destroy())  # Bind Escape key to close the window
        self.create_calculator_buttons()

    def create_calculator_buttons(self):
        calculator_names = ["Ohm's Law", "Wavelength"]
        for name in calculator_names:
            btn = ttk.Button(self.calc_window, text=name, width=20, command=lambda n=name: self.open_calculator(n))
            btn.pack(pady=5)

    def open_calculator(self, name):
        # messagebox.showinfo("Calculator", f"Opening {name} calculator (not implemented yet).")
        if name == "Ohm's Law":
            ohms_calculator = OhmsLawCalculator(self.parent)
            ohms_calculator.open_ohms_law_calculator()
        elif name == "Wavelength":
            wavelength_calculator = WavelengthCalculator(self.parent)
            wavelength_calculator.open_wavelength_calculator()

    def calculate_reduced_power(start_power_watts, db_reduction):
        """Calculates the target power needed after a specific dB reduction."""
        # Convert the dB reduction back to a raw power ratio
        # Ratio = 10^(dB / 10)
        power_ratio = 10 ** (db_reduction / 10)

        # Divide starting power by the ratio to get the target power
        target_power = start_power_watts / power_ratio
        return target_power
