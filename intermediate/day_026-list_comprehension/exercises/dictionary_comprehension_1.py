sentence = input()
# 🚨 Don't change code above 👆
# Write your code below 👇
result = {word: len(word) for word in sentence.split(' ')}

print(result)
