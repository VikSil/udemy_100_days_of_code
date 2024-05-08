from turtle import Turtle

LINK_SIZE = 20
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    def __init__(self):
        self.num_of_links = 3
        self.body = self.create_body()
        self.head = self.body[0]

    def create_body(self):
        body = []
        for x in range(self.num_of_links):
            body.append(Turtle())
            body[x].up()
            body[x].color('gray')
            body[x].shape('square')
            if x > 0:
                body[x].setx(x=body[x - 1].xcor() - LINK_SIZE)

        return body

    def move(self):
        for index, link in reversed(list(enumerate(self.body))):
            if index > 0:
                link.setx(x=self.body[index - 1].xcor())
                link.sety(y=self.body[index - 1].ycor())
            else:
                link.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() in [LEFT, RIGHT]:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() in [LEFT, RIGHT]:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() in [UP, DOWN]:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() in [UP, DOWN]:
            self.head.setheading(RIGHT)

    def dead(self) -> bool:
        if abs(self.head.xcor()) > 299 or abs(self.head.ycor()) > 299:
            return True
        for link in self.body[1:]:
            if self.head.distance(link) < 10:
                return True
        return False

    def grow(self):
        self.num_of_links += 1
        self.body.append(Turtle())
        tail = self.body[-1]
        tail.up()
        tail.color('gray')
        tail.shape('square')
        tail.goto(self.body[-2].position())
        tail.setheading = self.body[-2].heading()
