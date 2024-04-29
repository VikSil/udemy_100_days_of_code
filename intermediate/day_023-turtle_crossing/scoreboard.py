from turtle import Turtle

FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.level = 0
        self.up()
        self.goto(x= -290, y=260)
        self.hideturtle()
        self.refresh()

    def refresh(self):
        self.clear()
        self.write(f'Level: {self.level}', False, align='left', font=FONT)

    def level_up(self):
        self.level += 1
        self.refresh()

    def game_over(self):
        self.goto(0, 0)
        self.write('GAME OVER', False, align='center', font=FONT)
