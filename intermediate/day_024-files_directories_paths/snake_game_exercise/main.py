from turtle import Screen
import time

from snake import Snake
from food import Food
from scoreboard import Scoreboard


def main():

    screen = Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor('black')
    screen.title('Snake Game')
    screen.tracer(0)
    screen.colormode(255)

    snake = Snake()
    food = Food()
    score = Scoreboard()

    screen.listen()
    screen.onkey(key="Up", fun=snake.up)
    screen.onkey(key="Down", fun=snake.down)
    screen.onkey(key="Left", fun=snake.left)
    screen.onkey(key="Right", fun=snake.right)

    game_over = False
    while not game_over:
        screen.update()
        time.sleep(0.2)
        snake.move()

        if snake.head.distance(food) < 20:
            food.refresh()
            score.score += 1
            score.refresh()
            snake.grow()

        if snake.dead():
            snake.reset()
            score.reset()

    score.game_over()

    screen.exitonclick()


if __name__ == "__main__":
    main()
