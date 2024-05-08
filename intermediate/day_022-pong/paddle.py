from turtle import Turtle

NUM_OF_BLOCKS = 5
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Paddle(Turtle):

    def __init__(self, x_pos, y_pos, color):
        super().__init__()
        self.up()
        self.color(color)
        self.shape('square')
        self.shapesize(stretch_len=5, stretch_wid=1)
        self.setheading(UP)
        self.goto(x_pos, y_pos)

    def move_up(self):
        if self.ycor() < 240:
            self.setheading(UP)
            self.forward(20)

    def move_down(self):
        if self.ycor() > -240:
            self.setheading(DOWN)
            self.forward(20)
