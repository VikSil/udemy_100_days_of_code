# Reeborg's Hurdle Challenge


def turn_right():
    for i in range(0, 3):
        turn_left()


def jump():
    move()
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()


for i in range(0, 6):
    jump()


# -----------------------------------------

# Reebeorg's Hurdles Race - 1


def turn_right():
    for i in range(0, 3):
        turn_left()


def jump():
    move()
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()


while at_goal() != True:
    jump()


def turn_right():
    for i in range(0, 3):
        turn_left()


# -----------------------------------------

# Reebeorg's Hurdles Race - 2


def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()


while at_goal() != True:
    if front_is_clear() == True:
        move()
    else:
        jump()


# -----------------------------------------

# Reebeorg's Hurdles Race - 3


def turn_right():
    for i in range(0, 3):
        turn_left()


def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()


def move_up():
    while front_is_clear() == False:
        turn_left()
        move()
        turn_right()


def move_down():
    move()
    turn_right()
    while front_is_clear() == True:
        move()
    turn_left()


while at_goal() != True:
    if front_is_clear() == True:
        move()
    else:
        move_up()
        move_down()


# -----------------------------------------

# Reebeorg's Maze


def turn_right():
    for i in range(0, 3):
        turn_left()


def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()


while at_goal() != True:
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()
