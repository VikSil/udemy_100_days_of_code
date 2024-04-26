from turtle import Turtle, Screen


screen = Screen()
pen = Turtle()


def move_forward():
    pen.forward(10)


def move_backward():
    pen.backward(10)


def rotate_right():
    pen.right(10)


def rotate_left():
    pen.left(10)


def clear_screen():
    screen.resetscreen()


def main():

    screen.listen()

    screen.onkey(key="w", fun=move_forward)
    screen.onkey(key="s", fun=move_backward)
    screen.onkey(key="d", fun=rotate_right)
    screen.onkey(key="a", fun=rotate_left)
    screen.onkey(key="c", fun=clear_screen)

    screen.exitonclick()


if __name__ == "__main__":
    main()
