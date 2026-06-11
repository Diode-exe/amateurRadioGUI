"""Calculator window and controller for amateur radio tools."""

from tkinter import ttk
import tkinter as tk
from .ohms_law import OhmsLawCalculator
from .wavelength import WavelengthCalculator
from .reduced_power import ReducedPowerCalculator
from .frequency_meter import FrequencyMeterConverter


class Calculators:
    """Controller that opens lightweight calculator tools in separate windows.

    The class creates a small Toplevel containing buttons for each available
    calculator (Ohm's Law, Wavelength, Reduced Power, Frequency/Meter). Each
    button constructs and delegates to the corresponding calculator class.
    """

    def __init__(self, parent):
        """Initialize the calculators controller and show the selection window.

        Args:
            parent: The application GUI instance that contains `root`.
        """
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
        """Create and pack buttons for each available calculator.

        Buttons are created using `ttk.Button` and wired to `open_calculator`.
        """
        calculator_names = ["Ohm's Law", "Wavelength", "Reduced Power", "Frequency/Meter"]
        for name in calculator_names:
            btn = ttk.Button(self.calc_window, text=name, width=20, command=lambda n=name: self.open_calculator(n))
            btn.pack(pady=5)

    def open_calculator(self, name):
        """Instantiate and open the named calculator.

        Args:
            name: Human-readable name of the calculator to open.
        """
        # messagebox.showinfo("Calculator", f"Opening {name} calculator (not implemented yet).")
        if name == "Ohm's Law":
            ohms_calculator = OhmsLawCalculator(self.parent)
            ohms_calculator.open_ohms_law_calculator()
        elif name == "Wavelength":
            wavelength_calculator = WavelengthCalculator(self.parent)
            wavelength_calculator.open_wavelength_calculator()
        elif name == "Reduced Power":
            reduced_power_calculator = ReducedPowerCalculator(self.parent)
            reduced_power_calculator.open_reduced_power_calculator()
        elif name == "Frequency/Meter":
            frequency_meter_converter = FrequencyMeterConverter(self.parent)
            frequency_meter_converter.open_frequency_converter()