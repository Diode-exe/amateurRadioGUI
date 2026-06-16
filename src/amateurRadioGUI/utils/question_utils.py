"""Utility functions for question display and answer checking in the amateur radio GUI application."""

import random

class QuestionUtils:
    """Utility functions related to question display and answer checking."""
    def __init__(self):
        pass

    def show_random_question(self, gui_ref=None, hundred_random_questions_ref=None, current_question_index_ref=None):
        """Display the next question and present shuffled answer choices.

        This method updates the question label and radiobuttons with a new
        question taken from the pre-selected randomized list. The correct
        answer text is stored for later comparison in `check_answer()`.
        """
        gui_ref.check_answer_button.config(state="normal")
        gui_ref.next_button.config(state="disabled")
        # line to derive question and answer from
        # qa_derive_from = random.choice(self.hundred_random_questions).split(";")
        qa_derive_from = hundred_random_questions_ref[current_question_index_ref].split(";")
        four_answers = qa_derive_from[2:6]
        correct_answer = qa_derive_from[2].strip()
        question = qa_derive_from[1].strip()

        # print(question)
        # print(four_answers)
        # print(correct_answer)

        gui_ref.question_label.config(text=question)
        # shuffle the answers but keep the correct answer text for checking
        shuffled = four_answers.copy()
        random.shuffle(shuffled)
        gui_ref.correct_answer_text = correct_answer
        # clear selection and update radiobuttons
        gui_ref.selected_answer.set("")
        for i, btn in enumerate(gui_ref.choice_buttons):
            btn.config(text=shuffled[i])
            btn.deselect()
