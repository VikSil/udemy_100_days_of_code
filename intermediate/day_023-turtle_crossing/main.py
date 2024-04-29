import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

def main():
    screen = Screen()
    screen.setup(width=600, height=600)
    screen.title('Turtle Crossing')
    screen.tracer(0)

    turtle = Player()
    score = Scoreboard()
    cars = CarManager()

    screen.listen()
    screen.onkeypress(key="Up", fun=turtle.move)

    game_is_on = True
    while game_is_on:
        screen.update()
        time.sleep(0.1)
        cars.move_cars()
        cars.add_car()
        if turtle.arrived():
            score.level_up()
            cars.level_up()
            turtle.restart()
        game_is_on = not cars.detect_colision(turtle.xcor(), turtle.ycor())

    score.game_over()
    screen.exitonclick()


if __name__ == "__main__":
    main()
