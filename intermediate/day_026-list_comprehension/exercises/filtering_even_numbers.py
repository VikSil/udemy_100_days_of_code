list_of_strings = input().split(',')
# 🚨 Do  not change the code above

# TODO: Use list comprehension to convert the strings to integers 👇:
list_of_ints = [int(el) for el in list_of_strings]

# TODO: Use list comprehension to filter out the odd numbers
# and store the even numbers in a list called "result"
result = [el for el in list_of_ints if el % 2 == 0]

# Write your code 👆 above:
print(result)
