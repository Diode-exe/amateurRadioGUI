import tkinter as tk
from tkinter import messagebox, ttk

class OhmsLawCalculator:
    def __init__(self, parent):
        self.parent = parent
        self.ohms_window = None
        self.calculate_button = None
        self.voltage_entry = None
        self.current_entry = None
        self.resistance_entry = None
        self.final_result = None

    def open_ohms_law_calculator(self):
        self.ohms_window = tk.Toplevel(self.parent.root)
        self.ohms_window.title("Ohm's Law Calculator")
        self.ohms_window.geometry("300x250")
        self.ohms_window.transient(self.parent.root)
        self.ohms_window.lift()  # Bring the window to the front
        self.ohms_window.focus_force()  # Focus on the new window
        self.ohms_window.bind("<Return>", lambda event: self.calculate_button.invoke())  # Bind Enter key to calculate
        self.ohms_window.bind("<Escape>", lambda event: self.ohms_window.destroy())  # Bind Escape key to close the window

        tk.Label(self.ohms_window, text="Voltage (V):").grid(row=0, column=0, padx=5, pady=5)
        self.voltage_entry = tk.Entry(self.ohms_window)
        self.voltage_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.ohms_window, text="Current (I):").grid(row=1, column=0, padx=5, pady=5)
        self.current_entry = tk.Entry(self.ohms_window)
        self.current_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.ohms_window, text="Resistance (R):").grid(row=2, column=0, padx=5, pady=5)
        self.resistance_entry = tk.Entry(self.ohms_window)
        self.resistance_entry.grid(row=2, column=1, padx=5, pady=5)

        self.final_result = tk.StringVar()
        tk.Label(self.ohms_window, textvariable=self.final_result, font=("Arial", 12)).grid(row=4, columnspan=2, pady=10)

        self.calculate_button = ttk.Button(self.ohms_window, text="Calculate", command=self.calculate_ohms_law)
        self.calculate_button.grid(row=3, columnspan=2, pady=10)

    def calculate_ohms_law(self):
        try:
            V = float(self.voltage_entry.get()) if self.voltage_entry.get() else None
            I = float(self.current_entry.get()) if self.current_entry.get() else None
            R = float(self.resistance_entry.get()) if self.resistance_entry.get() else None

            if V is not None and I is not None:
                R = V / I
                # self.resistance_entry.delete(0, tk.END)
                self.final_result.set(f"Resistance (R): {R:.2f}")
            elif V is not None and R is not None:
                I = V / R
                # self.current_entry.delete(0, tk.END)
                self.final_result.set(f"Current (I): {I:.2f}")
            elif I is not None and R is not None:
                V = I * R
                # self.voltage_entry.delete(0, tk.END)
                self.final_result.set(f"Voltage (V): {V:.2f}")
            else:
                messagebox.showwarning("Input Error", "Please fill in exactly two fields.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
