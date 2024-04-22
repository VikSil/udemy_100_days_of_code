target = int(input())  # Enter a number between 0 and 1000
# 🚨 Do not change the code above ☝️

# Write your code here 👇

if target > 999:
    target = 999

sum = 0
for x in range(2, target + 1, 2):
    sum += x

print(sum)
