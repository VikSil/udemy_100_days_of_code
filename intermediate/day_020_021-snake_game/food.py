from turtle import Turtle
from random import randint


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("aqua")
        self.up()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.speed('fastest')
        x_coord = randint(-280, 280)
        y_coord = randint(-280, 250)
        self.goto(x=x_coord, y=y_coord)

    def refresh(self):
        x_coord = randint(-280, 280)
        y_coord = randint(-280, 280)
        self.goto(x=x_coord, y=y_coord)
