from turtle import Turtle, Screen
from random import randint
import colorgram
import os

screen = Screen()
pen = Turtle()


def get_colors():
    rgb_colors = []
    current_dir = os.path.dirname(os.path.realpath(__file__))
    colors = colorgram.extract(f'{current_dir}/image.jpg', 30)
    for color in colors:
        rgb_colors.append(
            (
                color.rgb.r,
                color.rgb.g,
                color.rgb.b,
            )
        )
    return rgb_colors


def line_of_dots(color_list, number_of_dots, radius, spacing):
    for _ in range(number_of_dots):
        pen.color(color_list[randint(0, len(color_list) - 1)])
        pen.dot(radius)
        pen.up()
        pen.forward(spacing + radius)
    pen.up()
    pen.back((spacing + radius) * number_of_dots)
    pen.left(90)
    pen.forward(spacing + round(0.5 * radius))
    pen.right(90)
    pen.down()


def main():

    screen.colormode(255)
    pen.speed('fastest')
    pen.hideturtle()
    pen.up()
    pen.goto(-400, -400)

    color_list = get_colors()
    for _ in range(10):
        line_of_dots(color_list, 10, 20, 50)

    screen.exitonclick()


if __name__ == "__main__":
    main()
