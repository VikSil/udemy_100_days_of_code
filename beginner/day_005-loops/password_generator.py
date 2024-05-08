# Password Generator Project
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

# Eazy Level - Order not randomised:
# e.g. 4 letter, 2 symbol, 2 number = JduE&!91
password1 = ''

for i in range(0, nr_letters):
    password1 += letters[random.randint(0, len(letters) - 1)]
for i in range(0, nr_symbols):
    password1 += symbols[random.randint(0, len(symbols) - 1)]
for i in range(0, nr_numbers):
    password1 += numbers[random.randint(0, len(numbers) - 1)]

print(f"Easy password generator: {password1}")

# Hard Level - Order of characters randomised:
# e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P

times = [nr_letters, nr_symbols, nr_numbers]
characters = [letters, symbols, numbers]
length = nr_letters + nr_symbols + nr_numbers
password2 = ''

for i in range(0, length):
    nextchar = False
    while not nextchar:
        r = random.randint(0, 2)
        if times[r] != 0:
            password2 += characters[r][random.randint(0, len(characters[r])) - 1]
            times[r] = times[r] - 1
            nextchar = True

print(f"Hard password generator: {password2}")
