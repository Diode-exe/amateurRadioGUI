import tkinter as tk

class ReducedPowerCalculator:
    def __init__(self, parent):
        self.parent = parent
        self.start_power_entry = None
        self.db_reduction_entry = None
        self.target_power_label = None
        self.calculate_button = None
        self.reduced_power_window = None

    def open_reduced_power_calculator(self):

        self.reduced_power_window = tk.Toplevel(self.parent.root)
        self.reduced_power_window.title("Reduced Power Calculator")
        self.reduced_power_window.geometry("300x150")
        self.reduced_power_window.transient(self.parent.root)
        self.reduced_power_window.lift()  # Bring the window to the front
        self.reduced_power_window.focus_force()  # Focus on the new window
        self.reduced_power_window.bind("<Return>", lambda event: self.calculate_button.invoke())  # Bind Enter key to calculate
        self.reduced_power_window.bind("<Escape>", lambda event: self.reduced_power_window.destroy())  # Bind Escape key to close the window

        self.start_power_entry = tk.Entry(self.reduced_power_window)
        self.start_power_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.reduced_power_window, text="Starting Power (Watts):").grid(row=0, column=0, padx=5, pady=5)
        self.db_reduction_entry = tk.Entry(self.reduced_power_window)
        self.db_reduction_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.reduced_power_window, text="dB Reduction:").grid(row=1, column=0, padx=5, pady=5)

        self.target_power_label = tk.Label(self.reduced_power_window, text="Target Power: 0 Watts")
        self.target_power_label.grid(row=3, columnspan=2, pady=5)

        self.calculate_button = tk.Button(self.reduced_power_window, text="Calculate", command=self.calculate_reduced_power)
        self.calculate_button.grid(row=2, columnspan=2, pady=10)

    def calculate_reduced_power(self):
        """Calculates the target power needed after a specific dB reduction."""
        # Convert the dB reduction back to a raw power ratio
        # Ratio = 10^(dB / 10)
        start_power_watts = float(self.start_power_entry.get())
        db_reduction = float(self.db_reduction_entry.get())
        power_ratio = 10 ** (db_reduction / 10)

        # Divide starting power by the ratio to get the target power
        target_power = start_power_watts / power_ratio
        self.target_power_label.config(text=f"Target Power: {target_power:.2f} Watts")
