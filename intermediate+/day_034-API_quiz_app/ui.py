from quiz_brain import QuizBrain
from pathlib import Path
from tkinter import *

THEME_COLOR = "#375362"
FONT_NAME = "Arial"
BASE_DIR = Path(__file__).resolve().parent


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title('Quizzler')
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text='Score: 0/1', font=(FONT_NAME, 15, 'bold'), bg=THEME_COLOR, fg='white')
        self.score_label.grid(column=1, row=0)

        self.canvas = Canvas(width=300, height=250, highlightthickness=0)
        self.question_txt = self.canvas.create_text(
            150,
            125,
            text='How many programmers does it take to screw in a lightbulb?',
            fill=THEME_COLOR,
            font=(FONT_NAME, 15, 'italic'),
            width=280,
        )
        self.canvas.grid(column=0, row=1, columnspan=2, pady=40)

        check_btn_img = PhotoImage(file=BASE_DIR / 'images/true.png')
        self.check_btn = Button(command=self.check_btn_click, image=check_btn_img, border=0, highlightthickness=0)
        self.check_btn.grid(column=0, row=2)

        x_btn_img = PhotoImage(file=BASE_DIR / 'images/false.png')
        self.x_btn = Button(command=self.x_btn_click, image=x_btn_img, border=0, highlightthickness=0)
        self.x_btn.grid(column=1, row=2)

        self.new_question()

        self.window.mainloop()

    def check_btn_click(self):
        is_correct = self.quiz.check_answer('True')
        self.feedback(is_correct)
        self.refresh_score()
        if self.quiz.still_has_questions():
            self.new_question()
        else:
            self.game_over()

    def x_btn_click(self):
        is_correct = self.quiz.check_answer('False')
        self.feedback(is_correct)
        self.refresh_score()
        if self.quiz.still_has_questions():
            self.new_question()
        else:
            self.game_over()

    def new_question(self):
        new_question_txt = self.quiz.next_question()
        self.canvas.itemconfig(self.question_txt, text=new_question_txt)

    def refresh_score(self):
        self.score_label.config(text=f'Score: {self.quiz.score}/{self.quiz.question_number}')

    def feedback(self, true_or_false):

        if true_or_false:
            self.canvas.config(bg="green")
            self.canvas.update_idletasks()
        else:
            self.canvas.config(bg="red")
            self.canvas.update_idletasks()

        self.window.after(1000, self.canvas.config(bg="white"))

    def game_over(self):
        self.canvas.itemconfig(self.question_txt, text='GAME OVER')
        self.canvas.config(bg="white")
        self.disable_buttons()

    def disable_buttons(self):
        self.x_btn['state'] = 'disabled'
        self.check_btn['state'] = 'disabled'
