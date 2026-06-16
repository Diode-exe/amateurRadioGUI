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

    def check_answer(self, gui_ref, script_dir_ref=None, timestamp_ref=None):
        """Evaluate the selected answer, show feedback, and save the result.
        Compares the user's selection to the stored correct answer, updates
        score counters, writes a record to a per-run answers file, and
        advances internal indices so the next question can be shown.
        """
        try:
            sel = gui_ref.selected_answer.get()
        except Exception as e:
            messagebox.showwarning("Selection error", f"An error occurred while getting the selection: {e}")
            return
        if not sel:
            messagebox.showwarning("No selection", "Please select an answer first.")
            return
        try:
            selected_index = int(sel)
        except ValueError:
            messagebox.showwarning("Selection error", "Invalid selection.")
            return
        selected_answer_text = gui_ref.choice_buttons[selected_index].cget("text").strip()
        correct_answer_text = gui_ref.correct_answer_text.strip()

        if selected_answer_text == correct_answer_text:
            messagebox.showinfo("Result", "Correct!")
            gui_ref.correct_count += 1
            gui_ref.check_answer_button.config(state="disabled")
            gui_ref.next_button.config(state="normal")
        else:
            messagebox.showinfo("Result", f"Wrong! The correct answer was: {correct_answer_text}")
            gui_ref.check_answer_button.config(state="disabled")
            gui_ref.next_button.config(state="normal")
        if script_dir_ref:
            try:
                os.makedirs(os.path.join(script_dir_ref, "data", "user_answers"), exist_ok=True)
                with open(os.path.join(script_dir_ref, "data", "user_answers", f"user_answers_{timestamp_ref}.txt"), "a", encoding="utf-8") as f:
                    f.write(f"Q: {gui_ref.question_label.cget('text')}\n")
                    f.write(f"Selected: {selected_answer_text}\n")
                    f.write(f"Correct: {correct_answer_text}\n\n")
                    f.write("-" * 40 + "\n\n")
            except Exception as e:
                messagebox.showerror("File Error", f"An error occurred while saving your answer: {e}")

        gui_ref.total_count += 1
        gui_ref.current_question_index += 1
        gui_ref.qa_so_far_var.set(f"Questions Answered: {gui_ref.total_count}")
        gui_ref.correct_so_far_var.set(f"Correct Answers: {gui_ref.correct_count}")
        gui_ref.next_button.config(state="normal")
        if gui_ref.total_count >= 100:
            messagebox.showinfo("Test Complete", f"You've completed the test! Your score: {gui_ref.correct_count}/100")
            gui_ref.check_answer_button.config(state="disabled")
            gui_ref.next_button.config(state="disabled")
