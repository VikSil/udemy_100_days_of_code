weather_c = eval(input())
# 🚨 Don't change code above 👆

# Write your code 👇 below:
weather_f = {key: (value * 9 / 5) + 32 for (key, value) in weather_c.items()}

print(weather_f)
