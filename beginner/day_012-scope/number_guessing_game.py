import random

def main():
    print('Welcome to the Number Guessing Game!')
    number = random.randint(1,101)
    print("I'm thinking of a number between 1 and 100.")
    difficulty = None
    while not difficulty:
        difficulty = input("Choose a dificulty. Type 'easy' or 'hard':")
        if difficulty != 'easy' and difficulty !='hard':
            difficulty = None
            print('Wrong input. Try again!')

    if difficulty == 'easy':
        attempts = 10
    else:
        attempts = 5
    print(f'You have {attempts} remaining to guess the number.')
    for x in range(attempts):
        guess = int(input('Make a guess:'))
        if guess == number:
            print(f'You got it! The answer was {number}.')
            return
        elif guess < number:
            print('Too low.')
        else:
            print('Too high.')
        if x < attempts - 1:
            print('Guess again.')
            print(f'You have {attempts-x-1} attempts remaining to guess the number.')
        else:
            print(f'The number was {number}')
            print("You've run out of guesses, you lose.")


if __name__ == "__main__":
    main()
