print("The Love Calculator is calculating your score...")
name1 = input()  # What is your name?
name2 = input()  # What is their name?
# 🚨 Don't change the code above 👆
# Write your code below this line 👇

both_names = (name1 + name2).replace(' ', '').lower()
first_digit = both_names.count('t') + both_names.count('r') + both_names.count('u') + both_names.count('e')
second_digit = both_names.count('l') + both_names.count('o') + both_names.count('v') + both_names.count('e')
score = int(str(first_digit) + str(second_digit))

if score < 10 or score > 90:
    print(f'Your score is {score}, you go together like coke and mentos.')
elif score >= 40 and score < 50:
    print(f'Your score is {score}, you are alright together.')
else:
    print(f'Your score is {score}.')
