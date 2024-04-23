# Write your code below this line 👇
import math


def prime_checker(number):
    is_prime = True
    for x in range(2, math.floor(number / 2)):
        if number % x == 0:
            is_prime = False
            break
    if is_prime:
        print("It's a prime number.")
    else:
        print("It's not a prime number.")


# Write your code above this line 👆

# Do NOT change any of the code below👇
n = int(input())  # Check this number
prime_checker(number=n)
