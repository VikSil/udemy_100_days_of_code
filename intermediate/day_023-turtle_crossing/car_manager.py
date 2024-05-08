from turtle import Turtle
from random import randint

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 5
LEFT = 180


class Car(Turtle):

    def __init__(self, step):
        super().__init__()
        self.up()
        color = COLORS[randint(0, len(COLORS) - 1)]
        self.color(color)
        self.shape('square')
        self.shapesize(stretch_len=2, stretch_wid=1)
        self.setheading(LEFT)
        y_coord = randint(-300, 300)
        self.goto(x=310, y=y_coord)
        self.step = step

    def move(self):
        self.forward(self.step)


class CarManager:

    def __init__(self):
        self.cars = []
        self.level = 0
        for _ in range(10):
            self.add_car()

    def add_car(self):
        coin_toss = randint(0, 1) and randint(0, 1) and randint(0, 1)
        if coin_toss:
            self.cars.append(Car(STARTING_MOVE_DISTANCE + self.level * MOVE_INCREMENT))

    def move_cars(self):
        for car in self.cars:
            car.move()

    def detect_colision(self, x_cord, y_cord):
        for car in self.cars:
            if abs(car.xcor() - x_cord) < 15 and abs(car.ycor() - y_cord) < 20:
                print('collided')
                return True
        return False

    def level_up(self):
        self.level += 1
