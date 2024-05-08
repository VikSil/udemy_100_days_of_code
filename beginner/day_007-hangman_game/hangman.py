from random import randint
import re
import hangman_art
import hangman_words


def printlist(list: list()):
    for i in list:
        print(f"{i.upper()} ", end='')
    print()


def print_hangman(lives):
    print(hangman_art.stages[lives])


def print_guessed(list: list()):
    print(f"Guessed letters: ", end='')
    for i in list:
        print(f"{i.upper()}, ", end='')
    print()


# initialise helper structures
letters = [
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]
guessed = []
lives = 6

# pick a word at from the list at random
word = hangman_words.word_list[randint(0, len(hangman_words.word_list) - 1)]
# create a copy of a hiden word to display to the user
word_copy = []
[word_copy.append("_") for character in word]

# print the game logo
print(hangman_art.logo)

# print the starting hangman
print(hangman_art.stages[-1])
printlist(word_copy)

# loop the game
keep_playing = True
while keep_playing:

    # defensively ask user for a new letter
    newletter = False
    while not newletter:
        print()
        guess = input("Guess a letter! \n").lower()
        if len(guess) == 1 and guess in letters:
            if guess not in guessed:
                newletter = True
                guessed.append(guess)
            else:
                print("You already guessed that letter")
        else:
            print("Only input letters, one letter at a time.")

    # check if the letter user guessed is in the word
    if guess in word:
        print("This letter is in the word.")
        placements = []
        placements = [character.start() for character in re.finditer(guess, word)]
        # reveal the letter in the word
        for p in placements:
            word_copy[p] = word[p]
        print_hangman(lives)
        printlist(word_copy)
        print_guessed(guessed)
    else:
        print("This letter is not in the word.")
        lives -= 1
        print_hangman(lives)
        printlist(word_copy)
        print_guessed(guessed)

    # check if the game should continue
    if not "_" in word_copy:
        print()
        print("You have won!")
        keep_playing = False
    elif lives == 0:
        word_copy = []
        word_copy = [letter for letter in word]
        print()
        print("You have died!")
        print("The word was:")
        printlist(word_copy)
        keep_playing = False
    else:
        continue
