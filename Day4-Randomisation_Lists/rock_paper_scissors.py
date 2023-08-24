from random import randint

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇

hands =[rock, paper, scissors]

while True:
    try:
        myhand = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors. "))
        if 0 <= myhand < 3:
            break
        else:
            print("Invalid input. Try again.")
    except:
        print("Invalid input. Try again.")

theirhand = randint(0,2)

print(hands[myhand])
print()
print("Computer chose:\n") 
print(hands[theirhand])
print()

if (myhand == 0 and theirhand == 1) | (myhand == 1 and theirhand == 2) | (myhand == 2 and theirhand == 1):
    print("You lose")
else:
    print("You win")