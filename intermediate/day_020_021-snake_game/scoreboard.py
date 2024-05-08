from turtle import Turtle

ALIGNMENT = 'center'
FONT = ('Corier New', 15, 'bold')


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.color('pink')
        self.up()
        self.goto(x=0, y=260)
        self.hideturtle()
        self.refresh()

    def refresh(self):
        self.clear()
        self.write(f'Score: {self.score}', False, align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write('GAME OVER', False, align=ALIGNMENT, font=FONT)
