from turtle import Turtle, Screen
from random import randint

screen = Screen()
pen = Turtle()

screen.colormode(255)
pen.shape('turtle')
pen.speed('fastest')

def draw_tringle():
    pen.color('violet')
    for _ in range(4):
        pen.forward(100)
        pen.right(90)

    screen.resetscreen()


def draw_dashed_line(num_of_steps, length_of_step):
    pen.left(15)
    pen.color('brown')
    for _ in range(num_of_steps):
        pen.forward(length_of_step)
        pen.up()
        pen.forward(length_of_step)
        pen.down()

    screen.resetscreen()


def draw_multi_shapes():
    pen.right(15)
    edges = 3
    for _ in range(8):
        angle = 360 / edges
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        pen.color((red, green, blue))
        for edge in range(edges):
            pen.forward(100)
            pen.right(angle)
        edges += 1

    screen.resetscreen()


def draw_random_walk(num_of_steps, length_of_step):
    directions = [0, 90, 180, 270]
    pen.width(10)
    for _ in range(num_of_steps):
        pen.color((randint(0, 255), randint(0, 255), randint(0, 255)))
        pen.setheading(directions[randint(0, 3)])
        pen.forward(length_of_step)

    screen.resetscreen()


def draw_spirograph(num_of_circles, radius):
    for _ in range(num_of_circles):
        pen.color((randint(0, 255), randint(0, 255), randint(0, 255)))
        pen.circle(radius)
        pen.right(round(360 / num_of_circles))

    screen.exitonclick()


def main():
    draw_tringle()
    draw_dashed_line(10,10)
    draw_multi_shapes()
    draw_random_walk(100,40)
    draw_spirograph(30, 100)


if __name__ == "__main__":
    main()
