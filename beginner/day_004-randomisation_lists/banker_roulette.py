names = names_string.split(", ")
# names_string contains the input values provided.
# The code above converts the input into an array seperating
# each name in the input by a comma and space.
# 🚨 Don't change the code above 👆

import random

num_of_people = len(names)
person_index = random.randint(1, num_of_people)
print(f'{names[person_index-1]} is going to buy the meal today!')
