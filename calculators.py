from tkinter import messagebox, ttk
import tkinter as tk

class Calculators:
    def __init__(self, parent):
        self.parent = parent
        self.calc_window = tk.Toplevel(self.parent.root)
        self.calc_window.title("Calculators")
        self.calc_window.geometry("300x200")
        self.calc_window.transient(self.parent.root)
        self.create_calculator_buttons()

    def create_calculator_buttons(self):
        calculator_names = ["Ohm's Law", "Wavelength"]
        for name in calculator_names:
            btn = ttk.Button(self.calc_window, text=name, width=20, command=lambda n=name: self.open_calculator(n))
            btn.pack(pady=5)

    def open_calculator(self, name):
        # messagebox.showinfo("Calculator", f"Opening {name} calculator (not implemented yet).")
        if name == "Ohm's Law":
            self.open_ohms_law_calculator()
        elif name == "Wavelength":
            self.open_wavelength_calculator()
            
    def open_ohms_law_calculator(self):
        ohms_window = tk.Toplevel(self.calc_window)
        ohms_window.title("Ohm's Law Calculator")
        ohms_window.geometry("300x250")
        ohms_window.transient(self.calc_window)
        ohms_window.lift()  # Bring the window to the front
        
        tk.Label(ohms_window, text="Voltage (V):").grid(row=0, column=0, padx=5, pady=5)
        voltage_entry = tk.Entry(ohms_window)
        voltage_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ohms_window, text="Current (I):").grid(row=1, column=0, padx=5, pady=5)
        current_entry = tk.Entry(ohms_window)
        current_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ohms_window, text="Resistance (R):").grid(row=2, column=0, padx=5, pady=5)
        resistance_entry = tk.Entry(ohms_window)
        resistance_entry.grid(row=2, column=1, padx=5, pady=5)
        
        final_result = tk.StringVar()
        tk.Label(ohms_window, textvariable=final_result, font=("Arial", 12)).grid(row=4, columnspan=2, pady=10)

        def calculate_ohms_law():
            try:
                V = float(voltage_entry.get()) if voltage_entry.get() else None
                I = float(current_entry.get()) if current_entry.get() else None
                R = float(resistance_entry.get()) if resistance_entry.get() else None

                if V is not None and I is not None:
                    R = V / I
                    # resistance_entry.delete(0, tk.END)
                    final_result.set(f"Resistance (R): {R:.2f}")
                elif V is not None and R is not None:
                    I = V / R
                    # current_entry.delete(0, tk.END)
                    final_result.set(f"Current (I): {I:.2f}")
                elif I is not None and R is not None:
                    V = I * R
                    # voltage_entry.delete(0, tk.END)
                    final_result.set(f"Voltage (V): {V:.2f}")
                else:
                    messagebox.showwarning("Input Error", "Please fill in exactly two fields.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")

        calculate_button = ttk.Button(ohms_window, text="Calculate", command=calculate_ohms_law)
        calculate_button.grid(row=3, columnspan=2, pady=10)
        
    def open_wavelength_calculator(self):
        wavelength_window = tk.Toplevel(self.calc_window)
        wavelength_window.title("Wavelength Calculator")
        wavelength_window.geometry("300x150")
        wavelength_window.transient(self.calc_window)
        wavelength_window.lift()  # Bring the window to the front
        
        tk.Label(wavelength_window, text="Frequency (MHz):").grid(row=0, column=0, padx=5, pady=5)
        frequency_entry = tk.Entry(wavelength_window)
        frequency_entry.grid(row=0, column=1, padx=5, pady=5)

        final_result = tk.StringVar()
        tk.Label(wavelength_window, textvariable=final_result, font=("Arial", 12)).grid(row=2, columnspan=2, pady=10)

        def calculate_wavelength():
            try:
                f = float(frequency_entry.get())
                if f <= 0:
                    messagebox.showerror("Input Error", "Frequency must be greater than zero.")
                    return
                c = 299792458  # speed of light in m/s
                wavelength = c / (f * 1e6)  # convert MHz to Hz
                final_result.set(f"Wavelength: {wavelength:.2f} meters")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number.")

        calculate_button = ttk.Button(wavelength_window, text="Calculate", command=calculate_wavelength)
        calculate_button.grid(row=1, columnspan=2, pady=10)