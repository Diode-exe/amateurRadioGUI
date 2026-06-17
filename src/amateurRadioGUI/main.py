"""Main GUI module for the Amateur Radio practice test application.

Provides the `GUI` class which manages the main window, question flow,
user interactions, and opening auxiliary tools (calculators and references).
"""

import os
import tkinter as tk
from tkinter import messagebox
import random
import datetime
from typing import Literal

from utils.network_utils import NetworkUtils
from utils.answer_utils import AnswerUtils
from utils.question_utils import QuestionUtils
from calculators.calcs import Calculators
from reference.q_codes import QCodes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Point precisely to the data folder
QUESTIONS_PATH = os.path.join(SCRIPT_DIR, "data", "questions.txt")
RANDOM_QUESTIONS_PATH = os.path.join(SCRIPT_DIR, "data", "random_questions.txt")

answer_utils = AnswerUtils()
question_utils = QuestionUtils()

class GUI:
    """Main application GUI for running the practice test.

    Responsibilities:
    - load question data and prepare a randomized subset
    - render the main Tkinter window and controls
    - handle answer selection, checking, and persistence of user answers
    """

    def __init__(self):
        """Initialize application state, load questions, and build the UI.

        Raises:
            FileNotFoundError: if the questions data file cannot be found.
        """
        # ------------------------
        self.calculators_frame = None
        self.calculators_button = None
        self.references_button = None
        self.dark_light_button = None
        self.question_label = None
        self.selected_answer = None
        self.choice_buttons = []
        self.qa_so_far_frame = None
        self.qa_so_far_var = None
        self.answer_so_far_label = None
        self.correct_so_far_var = None
        self.correct_so_far_label = None
        self.check_answer_button = None
        self.next_button = None
        self.timestamp = None
        # ------------------------
        self.correct_count = 0
        self.total_count = 0
        self.correct_answer_text = ""
        self.dark_mode = False
        try:
            with open(QUESTIONS_PATH, encoding="utf-8") as f:
                questions = [l for l in f.readlines() if l.strip()]
        except FileNotFoundError:
            if messagebox.askyesno("File Not Found", "The questions.txt file was not found.\n"
                                 "Would you like the program to download it?\n"):
                if messagebox.askyesnocancel("Download Questions", "Would you like basic or advanced questions?\n"
                                             "Yes for basic, No for advanced."):
                    url = "https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest.zip"
                else:
                    url = "https://apc-cap.ic.gc.ca/datafiles/amat_adv_quest.zip"

                network_utils = NetworkUtils()
                network_utils.download_questions(url)
                with open(QUESTIONS_PATH, encoding="utf-8") as f:
                    questions = [l for l in f.readlines() if l.strip()]

        self.hundred_random_questions = random.sample(questions, 100)

        with open(RANDOM_QUESTIONS_PATH, "w", encoding="utf-8") as f:
            f.writelines(self.hundred_random_questions)

        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        self.current_question_index = 0

        self.root = tk.Tk()
        self.root.title("Amateur Radio License Practice Test")
        self.root.geometry("500x400")
        self.root.state("zoomed")  # Start with zoomed window
        self.root.protocol("WM_DELETE_WINDOW", self.closer)

        self.bind_keys()
        self.bind_events()
        self.build_ui()

    def build_ui(self):
        """Construct the main window UI elements."""
        self.calculators_frame = tk.Frame(self.root)
        self.calculators_frame.pack(pady=10)

        # self.calculators = Calculators(self)
        self.calculators_button = tk.Button(self.calculators_frame, text="Open Calculators", command=lambda: self.open_window("calculators"))
        self.calculators_button.pack()

        self.q_codes_button = tk.Button(self.calculators_frame, text="Q-code References", command=lambda: self.open_window("q_codes"))
        self.q_codes_button.pack(pady=5)

        self.dark_light_button = tk.Button(self.calculators_frame, text="Toggle Dark/Light Mode", command=self.toggle_dark_light_mode)
        self.dark_light_button.pack(pady=5, side="right")

        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.selected_answer = tk.StringVar(value="")
        self.choice_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.root, text="", variable=self.selected_answer, value=str(i), font=("Arial", 12))
            btn.pack(anchor="w")
            self.choice_buttons.append(btn)
        self.choice_buttons[0].config(state="normal")

        self.qa_so_far_frame = tk.Frame(self.root)
        self.qa_so_far_frame.pack(pady=10)

        self.qa_so_far_var = tk.StringVar(self.qa_so_far_frame, value="Questions Answered: 0")
        self.answer_so_far_label = tk.Label(self.qa_so_far_frame, textvariable=self.qa_so_far_var, font=("Arial", 12))
        self.answer_so_far_label.pack(side="left", padx=10)

        self.correct_so_far_var = tk.StringVar(self.qa_so_far_frame, value="Correct Answers: 0")
        self.correct_so_far_label = tk.Label(self.qa_so_far_frame, textvariable=self.correct_so_far_var, font=("Arial", 12))
        self.correct_so_far_label.pack(side="left", padx=10)

        self.check_answer_button = tk.Button(self.root, text="Check Answer", command=self.user_clicks_check, disabledforeground="grey")
        self.check_answer_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next Question", command=self.load_question, state="disabled", disabledforeground="grey")
        self.next_button.pack(pady=10)
        # Ensure Next is disabled initially until an answer is checked
        self.next_button.config(state="disabled")

        # Load the first question into the UI
        # applying the returned data to widgets).
        self.load_question()

    def load_question(self):
        """Fetch question data from `question_utils` and apply to widgets.

        This method keeps all GUI updates local to the `GUI` class and
        advances `self.current_question_index` after successfully loading
        a question.
        """
        data = question_utils.get_question(self.hundred_random_questions, self.current_question_index)
        if not data:
            return

        self.question_label.config(text=data["question"])
        shuffled = data["choices"]
        self.correct_answer_text = data["correct"]
        # Clear selection and update radiobuttons
        self.selected_answer.set("")
        for i, btn in enumerate(self.choice_buttons):
            btn.config(text=shuffled[i])
            btn.deselect()

        # Advance the index so the next call loads the next question
        self.current_question_index += 1

        # Ensure button states reflect a freshly loaded question
        self.on_next_question()

    def bind_keys(self):
        """Bind keyboard shortcuts for answer selection and button actions."""
        self.root.bind("<Return>", self.enter_key_router)
        self.root.bind("1", lambda e: self.choice_buttons[0].invoke())
        self.root.bind("2", lambda e: self.choice_buttons[1].invoke())
        self.root.bind("3", lambda e: self.choice_buttons[2].invoke())
        self.root.bind("4", lambda e: self.choice_buttons[3].invoke())

    def bind_events(self):
        """Bind additional events for window management and interactions."""
        self.root.bind("<<AnswerChecked>>", self.on_answer_checked)
        self.root.bind("<<NextQuestion>>", self.on_next_question)
        self.root.bind("<<CorrectAnswer>>", self.correct_answer)

    # def open_calculators(self):
    #     """Open the calculators window (delegates to `Calculators`)."""
    #     Calculators(self)

    # def open_references(self):
    #     """Open the Q-code reference window (delegates to `QCodes`)."""
    #     QCodes(self)

    def open_window(self, window_name: Literal["calculators", "q_codes"]):
        """General method to open a new window based on the name."""
        if window_name == "calculators":
            Calculators(self)
        elif window_name == "q_codes":
            QCodes(self)

    def closer(self):
        """Prompt the user for confirmation and close the application."""
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.destroy()

    def enter_key_router(self, event): # pylint: disable=unused-argument
        """Handle the Enter key to either check the current answer or go next.

        Bound to the root window; chooses the appropriate action depending on
        which buttons are enabled.
        """
        if self.check_answer_button['state'] == 'normal':
            try:
                self.user_clicks_check()
            except Exception as e:
                print(f"Error in user_clicks_check: {e}")
                messagebox.showerror("Error", "An error occurred while checking the answer. Please try again.")

        elif self.next_button['state'] == 'normal':
            # Load the next question (GUI handles UI updates).
            self.load_question()
        else:
            # This case should not happen, but just in case both buttons are disabled, we can show a warning
            # hopefully this fixes a bug with the Enter key not working after switching windows
            messagebox.showwarning("Something went wrong", "Both buttons are disabled (for some reason). Please try again.")

    def toggle_dark_light_mode(self):
        """Toggle between dark and light mode for the application."""
        if self.dark_mode:
            # Switch to light mode
            self.root.config(bg="SystemButtonFace")
            self.question_label.config(bg="SystemButtonFace", fg="black")
            for btn in self.choice_buttons:
                btn.config(bg="SystemButtonFace", fg="black", selectcolor="SystemButtonFace")
            self.qa_so_far_frame.config(bg="SystemButtonFace")
            self.answer_so_far_label.config(bg="SystemButtonFace", fg="black")
            self.correct_so_far_label.config(bg="SystemButtonFace", fg="black")
            self.calculators_frame.config(bg="SystemButtonFace")
            self.calculators_button.config(bg="SystemButtonFace", fg="black")
            self.q_codes_button.config(bg="SystemButtonFace", fg="black")
            self.dark_light_button.config(bg="SystemButtonFace", fg="black")
        else:
            # Switch to dark mode
            self.root.config(bg="#2e2e2e")
            self.question_label.config(bg="#2e2e2e", fg="white")
            for btn in self.choice_buttons:
                btn.config(bg="#2e2e2e", fg="white", selectcolor="#4d4d4d")
            self.qa_so_far_frame.config(bg="#2e2e2e")
            self.answer_so_far_label.config(bg="#2e2e2e", fg="white")
            self.correct_so_far_label.config(bg="#2e2e2e", fg="white")
            self.calculators_frame.config(bg="#2e2e2e")
            self.calculators_button.config(bg="#4d4d4d", fg="white")
            self.q_codes_button.config(bg="#4d4d4d", fg="white")
            self.dark_light_button.config(bg="#4d4d4d", fg="white")
        self.dark_mode = not self.dark_mode

    def on_answer_checked(self, event=None):
        """Runs immediately after an answer is verified."""
        print("on_answer_checked handler called")
        self.total_count += 1
        self.qa_so_far_var.set(f"Questions Answered: {self.total_count}")
        self.correct_so_far_var.set(f"Correct Answers: {self.correct_count}")

        self.check_answer_button.config(state='disabled')
        # Ensure the visual contrast is clear on platforms/themes where
        # disabled buttons may look similar to enabled ones.
        self.check_answer_button.config(fg="grey")
        self.next_button.config(state='normal', fg="black")

        if self.total_count >= 100:
            messagebox.showinfo("Test Complete", f"You've completed the test! Your score: {self.correct_count}/100")
            self.check_answer_button.config(state="disabled")
            self.next_button.config(state="disabled")

        self.next_button.focus_set()  # Automatically shifts focus to the active button!
        # Force the UI to refresh so state changes are visible immediately
        try:
            self.root.update_idletasks()
        except Exception:
            pass

    def on_next_question(self, event=None):
        """Runs immediately when a fresh question loads."""
        print("on_next_question handler called")
        self.check_answer_button.config(state='normal', fg="black")
        self.next_button.config(state='disabled', fg="grey")
        self.check_answer_button.focus_set()  # Shifts focus back to the check button!
        try:
            self.root.update_idletasks()
        except Exception:
            pass

    def correct_answer(self, event=None):
        """Handle logic for when the user selects the correct answer."""
        messagebox.showinfo("Result", "Correct!")
        self.correct_count += 1
    
    def user_clicks_check(self):
        """Safely reads the selection and passes it to the utility file."""
        if not self.selected_answer.get():
            messagebox.showwarning("No Selection", "Please select an answer before checking.")
            return

        chosen_idx = int(self.selected_answer.get())
        chosen_text = self.choice_buttons[chosen_idx].cget("text").strip()

        answer_utils.check_answer(
            root_ref=self.root,
            sel_ref=chosen_text,
            correct_answer_text=self.correct_answer_text,
            question_text=self.question_label.cget("text"),
            script_dir_ref=SCRIPT_DIR,
            timestamp_ref=self.timestamp
        )

if __name__ == "__main__":
    gui = GUI()
    gui.root.protocol("WM_DELETE_WINDOW", gui.closer)
    gui.root.mainloop()
