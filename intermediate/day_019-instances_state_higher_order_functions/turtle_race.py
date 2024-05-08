from turtle import Turtle, Screen
from random import randint


screen = Screen()


def race(turtle: Turtle):
    step = randint(1, 100)
    turtle.forward(step)
    return turtle


def set_ready(colors: list[str]):

    turtles = []

    for x in range(len(colors)):
        turtles.append(Turtle())
        turtles[x].hideturtle()
        turtles[x].color(colors[x])
        turtles[x].shape('turtle')
        turtles[x].speed('slowest')
        turtles[x].up()
        turtles[x].goto(x=-400, y=-20 * x)
        turtles[x].showturtle()

    return turtles


def prepare_track(finishline: int):
    finish_line = Turtle()
    finish_line.hideturtle()
    finish_line.speed('slow')
    finish_line.up()
    finish_line.goto(finishline, -120)
    finish_line.down()
    finish_line.width(5)
    finish_line.left(90)
    finish_line.showturtle()
    finish_line.forward(200)
    finish_line.left(90)
    finish_line.forward(4)
    finish_line.color('red')
    finish_line.shape('triangle')


def main():

    screen.setup(width=1000, height=300)
    screen.ontimer(fun=None, t=200)  # wait 200ms before start execution

    colors = ['red', 'blue', 'green', 'orange', 'purple']
    turtles = set_ready(colors)

    finishline = 400
    prepare_track(finishline)
    racing = True

    bet = screen.textinput(title="Make your bet", prompt="Which color turtle will win the race? ")

    while racing:
        for turtle in turtles:
            turtle = race(turtle)
            if turtle.xcor() > finishline:
                winner = turtle.color()[0]
                print(f'The winner is {winner.capitalize()}!')
                if winner.lower() == bet.lower():
                    print('You were right!')
                else:
                    print('Your guess was wrong.')
                racing = False
                break

    screen.exitonclick()


if __name__ == "__main__":
    main()
