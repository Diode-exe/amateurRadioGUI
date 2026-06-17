"""Utility class for checking answers, providing feedback, and recording results."""

import os
from tkinter import messagebox

class AnswerUtils:
    """Utility class for handling answer checking, feedback, and recording.

    This class provides a method to evaluate the user's selected answer against
    the correct answer, display appropriate feedback, update score counters,
    and save the results to a file for later review.
    """
    def __init__(self):
        pass

    def check_answer(self, root_ref, sel_ref, correct_answer_text, question_text, script_dir_ref=None, timestamp_ref=None):
        """Evaluate the selected answer, show feedback, and save the result.
        Compares the user's selection to the stored correct answer, updates
        score counters, writes a record to a per-run answers file, and
        advances internal indices so the next question can be shown.
        """

        selected_answer_text = sel_ref.strip()
        correct_answer_text = correct_answer_text.strip()

        if selected_answer_text == correct_answer_text:
            root_ref.event_generate("<<CorrectAnswer>>")
        else:
            messagebox.showinfo("Result", f"Wrong! The correct answer was: {correct_answer_text}")

        if script_dir_ref:
            try:
                os.makedirs(os.path.join(script_dir_ref, "data", "user_answers"), exist_ok=True)
                with open(os.path.join(script_dir_ref, "data", "user_answers", f"user_answers_{timestamp_ref}.txt"), "a", encoding="utf-8") as f:
                    f.write(f"Q: {question_text}\n")
                    f.write(f"Correct: {correct_answer_text}\n\n")
                    f.write(f"Selected: {selected_answer_text}\n")
                    f.write("-" * 40 + "\n\n")
            except Exception as e:
                messagebox.showerror("File Error", f"An error occurred while saving your answer: {e}")

        root_ref.event_generate("<<AnswerChecked>>")
