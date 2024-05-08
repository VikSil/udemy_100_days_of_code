from turtle import Turtle
from random import randint


DIAMETER = 20


class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("aqua")
        self.up()
        self.x_step = 0
        self.y_step = 0
        self.restart()

    def move(self):
        next_x = self.xcor() + self.x_step
        next_y = self.ycor() + self.y_step
        self.goto(x=next_x, y=next_y)
        self.bounce_off_wall()

    def bounce_off_wall(self):
        if abs(self.ycor()) > 281:
            self.y_step *= -1

    def bounce_off_paddle(self):
        if abs(self.xcor()) > 281:
            self.x_step *= -1

    def restart(self):
        self.goto(x=0, y=0)
        self.x_step = 0
        self.y_step = 0
        while self.x_step == 0:
            self.x_step = randint(-5, 5)
        while self.y_step == 0:
            self.y_step = randint(-5, 5)
