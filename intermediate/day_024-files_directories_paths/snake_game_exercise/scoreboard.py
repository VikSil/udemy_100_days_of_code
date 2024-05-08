from turtle import Turtle
import os

ALIGNMENT = 'center'
FONT = ('Corier New', 15, 'bold')


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.color('pink')
        self.up()
        self.goto(x=0, y=260)
        self.hideturtle()
        self.refresh()

    def refresh(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(f'{current_dir}/high_score.txt') as file:
            self.high_score = int(file.read())
        self.clear()
        self.write(f'Score: {self.score} | High Score: {self.high_score}', False, align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            current_dir = os.path.dirname(os.path.realpath(__file__))
            with open(f'{current_dir}/high_score.txt', mode='w') as file:
                file.write(str(self.high_score))

        self.score = 0
        self.refresh()
