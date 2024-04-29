import time
from turtle import Screen

from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard


def main():

    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor('black')
    screen.title('PONG')
    screen.tracer(0)
    screen.colormode(255)

    left_paddle = Paddle(-350, 0, 'red')
    right_paddle = Paddle(350, 0, 'blue')
    ball = Ball()
    score = Scoreboard()

    screen.listen()
    screen.onkeypress(key="Up", fun=right_paddle.move_up)
    screen.onkeypress(key="Down", fun=right_paddle.move_down)
    screen.onkeypress(key="w", fun=left_paddle.move_up)
    screen.onkeypress(key="x", fun=left_paddle.move_down)

    game_over = False
    while not game_over:
        screen.update()
        time.sleep(0.01)
        ball.move()

        if ball.distance(right_paddle) < 55 and ball.xcor() > 330 and ball.xcor() < 350 and ball.x_step > 0:
            ball.bounce_off_paddle()

        if ball.distance(left_paddle) < 55 and ball.xcor() < -330 and ball.xcor() > -350 and ball.x_step < 0:
            ball.bounce_off_paddle()

        if ball.xcor() > 405:
            score.left_score += 1
            score.refresh()
            ball.restart()
            time.sleep(1)

        if ball.xcor() < -411: # screen works differently on right and left side for some reason
            score.right_score += 1
            score.refresh()
            ball.restart()
            time.sleep(1)

        if score.left_score == 10 or score.right_score == 10:
            game_over = True
            ball.x_step = 0
            ball.y_step = 0
            ball.restart()
            score.game_over()

    screen.exitonclick()


if __name__ == "__main__":
    main()
