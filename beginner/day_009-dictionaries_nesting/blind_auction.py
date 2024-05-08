from replit import clear


# find the highest amongst values in the dictionary
def winner(bidders: dict):
    return max(bidders, key=bidders.get)


print("Welcome to the secret auction program.")

bidders = {}
end = False
# loop while more bidders remain
while not end:
    name = input("What is your name?: ")
    try:
        bid = int(input("What's your bid?: $"))
    except:
        print("Bad bid! You are disqualified.")
    bidders[name] = bid

    # ask if there are any more bidders
    response = False
    while not response:
        next = input("Are there any other bidders? Type 'yes' or 'no'.\n")
        if (next.lower() == 'yes') or (next.lower() == 'y'):
            # clear the screen if there are any more bidders
            clear()
            response = True
        # if no more bidders, find who bid the highest
        elif (next.lower() == 'no') or (next.lower() == 'n'):
            winner = winner(bidders)
            print(f"The winner is {winner} with a bid of ${bidders[winner]}.")
            response = True
            end = True
        else:
            print("Invalid Input.")
