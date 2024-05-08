print(
    '''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
'''
)
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

# https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Treasure%20Island%20Conditional.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1oDe4ehjWZipYRsVfeAx2HyB7LCQ8_Fvi%26export%3Ddownload

# Write your code below this line 👇

while True:
    direction = input("You are at a crossroads. Do you want to go left (L) or right (R)? ")
    if (
        direction.lower() == "r"
        or direction.lower() == "l"
        or direction.lower() == "right"
        or direction.lower() == "left"
    ):
        break
    else:
        print("Invalid input, try again.")

# went right
if direction.lower() == "r" or direction.lower() == "right":
    print("You fell into a hole and died. Game Over!")
# went left
else:
    while True:
        lake = input(
            "You come to a lake. There is an island in the middle of the lake. Do you wait(W) for a boat or swim(S) across? "
        )
        if lake.lower() == "w" or lake.lower() == "s" or lake.lower() == "wait" or lake.lower() == "swim":
            break
        else:
            print("Invalid input, try again.")
    # swam
    if lake.lower() == "s" or lake.lower() == "swim":
        print("A giant trout ate you. Game Over!")
    # waited for boat
    else:
        while True:
            door = input(
                "You arrive at the island unharmed. There is a house with 3 doors. One red (R), one yellow (Y) and one blue (B). Which door do you choose? "
            )
            if (
                door.lower() == "r"
                or door.lower() == "y"
                or door.lower() == "b"
                or door.lower() == "red"
                or door.lower() == "yellow"
                or door.lower() == "blue"
            ):
                break
            else:
                print("Invalid input, try again.")
        # chose red
        if door.lower() == "r" or door.lower() == "red":
            print("The room was on fire and you were burnt alive. Game Over!")
        # chose blue
        elif door.lower() == "b" or door.lower() == "blue":
            print("Blue beasts behind the door ate you alive. Game Over!")
        # chose yellow
        else:
            print("You found the treasure. Congratulations! But it is still - Game Over!")
