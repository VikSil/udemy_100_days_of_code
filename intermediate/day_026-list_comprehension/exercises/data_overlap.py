f1 = open("file1.txt", "r")
list_a = f1.readlines()
list_a = [int(el.strip()) for el in list_a]

f2 = open("file2.txt", "r")
list_b = f2.readlines()
list_b = [int(el.strip()) for el in list_b]

result = [el for el in list_a if el in list_b]

# Write your code above 👆
print(result)
