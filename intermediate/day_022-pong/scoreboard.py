from turtle import Turtle

ALIGNMENT = 'center'
FONT = ('Corier New', 25, 'bold')


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.left_score = 0
        self.right_score = 0
        self.color('yellow')
        self.up()
        self.goto(x=0, y=260)
        self.hideturtle()
        self.refresh()

    def refresh(self):
        self.clear()
        self.write(f'{self.left_score} : {self.right_score}', False, align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write('GAME OVER', False, align=ALIGNMENT, font=FONT)
