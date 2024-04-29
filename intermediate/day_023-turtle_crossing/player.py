from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280
UP = 90


class Player(Turtle):
    
    def __init__(self):
        super().__init__()
        self.up()
        self.shape('turtle')
        self.setheading(UP)
        self.restart()

    def move(self):
        self.forward(MOVE_DISTANCE)

    def arrived(self):
        if self.ycor() >= FINISH_LINE_Y:
            return True
        return False

    def restart(self):
        self.goto(STARTING_POSITION)
