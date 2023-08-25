from random import randint
import re

def printlist(list:list()):
    print()
    for i in list:
        
        print(f"{i.upper()} ", end = '')
    print()


#initialise helper structures
word_list = ["aardvark", "baboon", "camel"]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
guessed = []
lives = 6

stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

#pick a word at from the list at random
word = word_list[randint(0,len(word_list)-1)]
#create a copy of a hiden word to display to the user
word_copy = []
[word_copy.append("_") for character in word]

#print the starting hangman
print(stages[0])
printlist(word_copy)

#loop the game
keep_playing = True
while keep_playing:

#defensively ask user for a new letter
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

#check if the letter user guessed is in the word
    if guess in word:
        print("This letter is in the word.")
        placements = []
        placements = [character.start() for character in re.finditer(guess, word) ]
        #reveal the letter in the word
        for p in placements:
            word_copy[p] = word[p]    
        print(stages[(len(stages)-1)-lives])
        printlist(word_copy)
    else:
        print("This letter is not in the word.")
        lives -=1
        print(stages[(len(stages)-1)-lives])
        printlist(word_copy)

#check if the game should continue
    if not "_" in word_copy:
        print("You have won!")
        keep_playing = False
    elif lives == 0:
        print("You have died!")
        keep_playing = False
    else:
        continue