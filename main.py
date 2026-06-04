import tkinter as tk
from tkinter import messagebox
import random
import datetime

from calculators import Calculators

class GUI:
    def __init__(self):
        self.correct_count = 0
        self.total_count = 0
        self.correct_answer_text = ""
        questions = [l for l in open("questions.txt", encoding="utf-8").readlines() if l.strip()]

        self.hundred_random_questions = random.sample(questions, 100)
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
        
        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.selected_answer = tk.StringVar()
        self.selected_answer.set("")
        self.choice_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.root, text="", variable=self.selected_answer, value=str(i), font=("Arial", 12))
            btn.pack(anchor="w")
            self.choice_buttons.append(btn)
        self.choice_buttons[0].config(state="active")

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
        self.check_answer_button.config(state="active")
        self.next_button.config(state="disabled")
        # line to derive question and answer from
        qa_derive_from = random.choice(self.hundred_random_questions).split(";")
        four_answers = qa_derive_from[2:6]
        correct_answer = qa_derive_from[2].strip()
        question = qa_derive_from[1].strip()

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
        else:
            messagebox.showinfo("Result", f"Wrong! The correct answer was: {correct_answer_text}")
            self.check_answer_button.config(state="disabled")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"user_answers_{timestamp}.txt", "a", encoding="utf-8") as f:
            f.write(f"Q: {self.question_label.cget('text')}\n")
            f.write(f"Selected: {selected_answer_text}\n")
            f.write(f"Correct: {correct_answer_text}\n\n")
            f.write("-" * 40 + "\n\n")

        self.total_count += 1
        self.qa_so_far_var.set(f"Questions Answered: {self.total_count}")
        self.correct_so_far_var.set(f"Correct Answers: {self.correct_count}")
        self.next_button.config(state="active")
        if self.total_count >= 100:
            messagebox.showinfo("Test Complete", f"You've completed the test! Your score: {self.correct_count}/100")
            self.check_answer_button.config(state="disabled")
            self.next_button.config(state="disabled")
        
    def open_calculators(self):
        calcu = Calculators(self)
    
    def closer(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.destroy()
            
    def enter_check_next(self, event):
        if self.check_answer_button['state'] == 'active':
            self.check_answer()
        elif self.next_button['state'] == 'active':
            self.show_random_question()

if __name__ == "__main__":
    gui = GUI()
    gui.root.protocol("WM_DELETE_WINDOW", gui.closer)
    gui.root.mainloop()