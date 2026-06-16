"""Main GUI module for the Amateur Radio practice test application.

Provides the `GUI` class which manages the main window, question flow,
user interactions, and opening auxiliary tools (calculators and references).
"""

import json
import os
import tkinter as tk
from tkinter import messagebox
import random
import datetime

from utils.network_utils import NetworkUtils
from calculators.calcs import Calculators
from reference.q_codes import QCodes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Point precisely to the data folder
QUESTIONS_PATH = os.path.join(SCRIPT_DIR, "data", "questions.txt")
RANDOM_QUESTIONS_PATH = os.path.join(SCRIPT_DIR, "data", "random_questions.txt")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config", "config.json")

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
        self.correct_count = 0
        self.total_count = 0
        self.correct_answer_text = ""
        self.dark_mode = False
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                config = json.load(f)
                self.french_mode = config.get("french_mode", False)
        except FileNotFoundError:
            self.french_mode = False

        if not self.french_mode:
            # english mode
            self.question_index = 1
            self.correct_answer_index = 2
            self.four_answers_start_index = 2
            self.four_answers_end_index = 5
        else:
            self.question_index = 6
            self.correct_answer_index = 7
            self.four_answers_start_index = 7
            self.four_answers_end_index = 11
            # correct_answer = qa_derive_from[2].strip()
            # four_answers = qa_derive_from[2:6]

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
        self.root.bind("<Return>", self.enter_check_next)
        self.root.bind("1", lambda e: self.choice_buttons[0].invoke())
        self.root.bind("2", lambda e: self.choice_buttons[1].invoke())
        self.root.bind("3", lambda e: self.choice_buttons[2].invoke())
        self.root.bind("4", lambda e: self.choice_buttons[3].invoke())

        self.calculators_frame = tk.Frame(self.root)
        self.calculators_frame.pack(pady=10)

        # self.calculators = Calculators(self)
        self.calculators_button = tk.Button(self.calculators_frame, text="Open Calculators", command=self.open_calculators)
        self.calculators_button.pack()

        self.references_button = tk.Button(self.calculators_frame, text="Q-code References", command=self.open_references)
        self.references_button.pack(pady=5)

        self.dark_light_button = tk.Button(self.calculators_frame, text="Toggle Dark/Light Mode", command=self.toggle_dark_light_mode)
        self.dark_light_button.pack(pady=5, side="right")

        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.selected_answer = tk.StringVar()
        self.selected_answer.set("")
        self.choice_buttons = []
        if not self.french_mode:
            # english mode
            for i in range(4):
                btn = tk.Radiobutton(self.root, text="", variable=self.selected_answer, value=str(i), font=("Arial", 12))
                btn.pack(anchor="w")
                self.choice_buttons.append(btn)
        else:
            for i in range(8, 12):
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

        self.check_answer_button = tk.Button(self.root, text="Check Answer", command=self.check_answer)
        self.check_answer_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next Question", command=self.show_random_question)
        self.next_button.pack(pady=10)

        self.show_random_question()

    def show_random_question(self):
        """Display the next question and present shuffled answer choices.

        This method updates the question label and radiobuttons with a new
        question taken from the pre-selected randomized list. The correct
        answer text is stored for later comparison in `check_answer()`.
        """
        self.check_answer_button.config(state="normal")
        self.next_button.config(state="disabled")
        # line to derive question and answer from
        # qa_derive_from = random.choice(self.hundred_random_questions).split(";")
        qa_derive_from = self.hundred_random_questions[self.current_question_index].split(";")
        # print(f"DEBUG: qa_derive_from = {qa_derive_from}")  # Debug print to check the structure of the question data
        question = qa_derive_from[self.question_index].strip()
        # print(f"DEBUG: question = {question}")  # Debug print to check the extracted question
        correct_answer = qa_derive_from[self.correct_answer_index].strip()
        # print(f"DEBUG: correct_answer = {correct_answer}")  # Debug print to check the extracted correct answer
        four_answers = qa_derive_from[self.four_answers_start_index:self.four_answers_end_index]
        # print(f"DEBUG: four_answers = {four_answers}")  # Debug print to check the extracted answer choices

        # print(question)
        # print(four_answers)
        # print(correct_answer)

        self.question_label.config(text=question)
        # shuffle the answers but keep the correct answer text for checking
        shuffled = four_answers.copy()
        random.shuffle(shuffled)
        self.correct_answer_text = correct_answer
        # clear selection and update radiobuttons
        self.selected_answer.set("")
        for i, btn in enumerate(self.choice_buttons):
            btn.config(text=shuffled[i])
            btn.deselect()

    def check_answer(self):
        """Evaluate the selected answer, show feedback, and save the result.

        Compares the user's selection to the stored correct answer, updates
        score counters, writes a record to a per-run answers file, and
        advances internal indices so the next question can be shown.
        """
        sel = self.selected_answer.get()
        if not sel:
            messagebox.showwarning("No selection", "Please select an answer first.")
            return
        try:
            selected_index = int(sel)
        except ValueError:
            messagebox.showwarning("Selection error", "Invalid selection.")
            return
        selected_answer_text = self.choice_buttons[selected_index].cget("text").strip()
        correct_answer_text = self.correct_answer_text.strip()

        if selected_answer_text == correct_answer_text:
            messagebox.showinfo("Result", "Correct!")
            self.correct_count += 1
            self.check_answer_button.config(state="disabled")
            self.next_button.config(state="normal")
        else:
            messagebox.showinfo("Result", f"Wrong! The correct answer was: {correct_answer_text}")
            self.check_answer_button.config(state="disabled")
            self.next_button.config(state="normal")

        try:
            os.makedirs(os.path.join(SCRIPT_DIR, "data", "user_answers"), exist_ok=True)
            with open(os.path.join(SCRIPT_DIR, "data", "user_answers", f"user_answers_{self.timestamp}.txt"), "a", encoding="utf-8") as f:
                f.write(f"Q: {self.question_label.cget('text')}\n")
                f.write(f"Selected: {selected_answer_text}\n")
                f.write(f"Correct: {correct_answer_text}\n\n")
                f.write("-" * 40 + "\n\n")
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while saving your answer: {e}")

        self.total_count += 1
        self.current_question_index += 1
        self.qa_so_far_var.set(f"Questions Answered: {self.total_count}")
        self.correct_so_far_var.set(f"Correct Answers: {self.correct_count}")
        self.next_button.config(state="normal")
        if self.total_count >= 100:
            messagebox.showinfo("Test Complete", f"You've completed the test! Your score: {self.correct_count}/100")
            self.check_answer_button.config(state="disabled")
            self.next_button.config(state="disabled")

    def open_calculators(self):
        """Open the calculators window (delegates to `Calculators`)."""
        calcu = Calculators(self)

    def open_references(self):
        """Open the Q-code reference window (delegates to `QCodes`)."""
        q_codes_ref = QCodes(self)

    def closer(self):
        """Prompt the user for confirmation and close the application."""
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.destroy()

    def enter_check_next(self, event):
        """Handle the Enter key to either check the current answer or go next.

        Bound to the root window; chooses the appropriate action depending on
        which buttons are enabled.
        """
        if self.check_answer_button['state'] == 'normal':
            self.check_answer()
        elif self.next_button['state'] == 'normal':
            self.show_random_question()
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
            self.references_button.config(bg="SystemButtonFace", fg="black")
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
            self.references_button.config(bg="#4d4d4d", fg="white")
            self.dark_light_button.config(bg="#4d4d4d", fg="white")
        self.dark_mode = not self.dark_mode

if __name__ == "__main__":
    gui = GUI()
    gui.root.protocol("WM_DELETE_WINDOW", gui.closer)
    gui.root.mainloop()