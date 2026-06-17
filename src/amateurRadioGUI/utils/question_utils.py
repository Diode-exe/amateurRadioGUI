"""Utility functions for question display and answer checking in the amateur radio GUI application."""

import random

class QuestionUtils:
    """Utility functions related to question data handling.

    This class is GUI-agnostic: it provides pure helpers that return
    question data (text, choices, correct answer) so the caller (the
    GUI) can update widgets on the main thread. No Tkinter or UI code
    should exist in this module.
    """

    def __init__(self):
        pass

    def get_question(self, hundred_random_questions, index):
        """Return question data for the given index.

        Args:
            hundred_random_questions: list of question lines (pre-shuffled)
            index: integer index of the question to return

        Returns:
            dict with keys: 'question', 'choices', 'correct', or None if
            index is out of range.
        """
        if not hundred_random_questions or index < 0 or index >= len(hundred_random_questions):
            return None

        qa_derive_from = hundred_random_questions[index].split(";")
        question = qa_derive_from[1].strip()
        answers = qa_derive_from[2:6]
        correct = qa_derive_from[2].strip()
        shuffled = answers.copy()
        random.shuffle(shuffled)

        return {
            "question": question,
            "choices": shuffled,
            "correct": correct,
        }
    
