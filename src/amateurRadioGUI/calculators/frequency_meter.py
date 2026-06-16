"""Frequency / Wavelength converter UI for the amateurRadioGUI app.

This module provides `FrequencyMeterConverter`, a small Tkinter-based
converter that lets the user convert between frequency in MHz and
wavelength in meters. The UI is opened as a transient `Toplevel` window
attached to the application's main `root` window.
"""

import tkinter as tk
from tkinter import ttk

class FrequencyMeterConverter:
    """UI helper for converting between MHz and meters.

    The `parent` argument should be the main application object that
    exposes a `root` attribute (the Tk root window). Instances create a
    transient `Toplevel` window with input fields for either frequency
    (MHz) or wavelength (meters) and show the converted result.
    """

    def __init__(self, parent):
        """Initialize the converter helper.

        Args:
            parent: The main application object; expected to have a
                `root` attribute referencing the Tk root window. The
                converter stores references to the UI widgets it
                creates so they can be queried and updated later.
        """
        self.parent = parent
        self.frequency_entry = None
        self.result_label = None
        self.convert_button = None
        self.converter_window = None
        self.meters_entry = None

    def open_frequency_converter(self):
        """Create and display the converter window.

        This method builds a transient `Toplevel` window attached to the
        parent's root window. The window contains two mutually exclusive
        input fields: one for frequency in MHz and one for wavelength in
        meters. Pressing Enter triggers conversion; pressing Escape
        closes the window. The converted result is displayed in
        `self.result_label`.
        """
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
        """Read inputs, perform conversion, and display the result.

        Conversion formulas used:
        - wavelength (meters) = 300 / frequency (MHz)
        - frequency (MHz) = 300 / wavelength (meters)

        Behavior:
        - If both input fields contain values, an error dialog is shown
          asking the user to fill only one field.
        - If the frequency field contains a valid number, compute the
          wavelength and update `self.result_label`.
        - If the meters field contains a valid number, compute the
          frequency and update `self.result_label`.
        - If neither field contains a value, or if parsing fails, an
          error dialog is shown explaining the problem.
        """
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
