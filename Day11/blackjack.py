import sys
import os

# import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import helper_functions  # all functions that are passed to defensive_while need to return a list with True as first element to break out
from replit import clear

from logo import logo
from random import randint


############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

################# Requirements ################################

# Deal both user and computer a starting hand of 2 random card values.
# Detect when computer or user has a blackjack. (Ace + 10 value card).
# If computer gets blackjack, then the user loses (even if the user also has a blackjack). If the user gets a blackjack, then they win (unless the computer also has a blackjack).
# Calculate the user's and computer's scores based on their card values.
# If an ace is drawn, count it as 11. But if the total goes over 21, count the ace as 1 instead.
# Reveal computer's first card to the user.
# Game ends immediately when user score goes over 21 or if the user or computer gets a blackjack.
# Ask the user if they want to get another card.
# Once the user is done and no longer wants to draw any more cards, let the computer play. The computer should keep drawing cards unless their score goes over 16.
# Compare user and computer scores and see if it's a win, loss, or draw.
# Print out the player's and computer's final hand and their scores at the end of the game.

###############################################################

def draw_random():
    return cards[randint(0, 12)]

def draw_again():
    again = input("Type 'y' to get another card, type 'n' to pass: ")
    # if yes - next round - True
    if again.lower() == "y":
        return list([True, True])
    # if no - next round - False
    elif again.lower() == "n":
        return list([True, False])
    else:
        print("Wrong input. Try again")

def special_sum(some_hand: list):
    if sum(some_hand) < 22 or 11 not in some_hand:
        return sum(some_hand)
    return sum(some_hand)-10

def gone_over(hand: list):
    if special_sum(hand) > 21:
        return True
    return False
    
def  end_game(both_hands:dict):
    #reveal computer's hand
    print(f"Dealer's cards: {both_hands['deal_hand']}, score: {special_sum(both_hands['deal_hand'])}")

    #user overrun their hand - automatic loss
    if special_sum(both_hands["my_hand"]) > 21:
        sys.exit ("You lose. Game over")
    #user aced - loose if computer also aced, otherwise win
    elif special_sum(both_hands["my_hand"]) == 21:
        if special_sum(both_hands["deal_hand"]) == 21:
            sys.exit  ("You lose. Game over")
        else:
            sys.exit ("You win!")
    #user didn't ace - compare scores
    else:
        #computer overrun - user wins
        if special_sum(both_hands["deal_hand"]) > 21:
            sys.exit ("You win!")
        #computer aced - user looses
        elif special_sum(both_hands["deal_hand"]) == 21:
            sys.exit ("You lose. Game over")
        #user scored higher than computer - user wins
        elif special_sum(both_hands["my_hand"]) > special_sum(both_hands["deal_hand"]):
            sys.exit ("You win!")
        #user scored less than computer - user looses
        else:
            sys.exit ("You lose. Game over")



def round(counter, hands):

    # print(f"BTW, counter is {counter}")
    # print(f"BTW, my hand: {hands['my_hand']}")
    # print(f"BTW, deal hand: {hands['deal_hand']}")

    #draws card to each hand twice
    if counter < 2:
        hands["my_hand"].append(draw_random())
        hands["deal_hand"].append(draw_random())
        counter +=1
        round(counter, hands)

    #user's rounds
    elif counter < 12: #theoretically user could get 2 * 10 before overruning
        #tell the user his hand and first card in computer's hand
        print(f"Your cards: {hands['my_hand']}, current score: {special_sum(hands['my_hand'])}")
        
        #check if user gone over - end game if they have
        if gone_over(hands['my_hand']):
            end_game(hands)
        #if user aced - end game    
        if special_sum(hands["my_hand"]) == 21:
            end_game(hands)

        print(f"Dealer's first card: {hands['deal_hand'][0]}")


        #ask user if they want to draw again
        next_round, = helper_functions.defensive_while(draw_again)
        #if user want to draw, then draw and go to next round
        if next_round:
            hands["my_hand"].append(draw_random())
            counter +=1
            round(counter, hands)
        # if user does not want to draw, go to computer's rounds
        else:
            counter = 13
            round(counter, hands)

    #computer's rounds
    else:
        #if computer aced - end game
        if special_sum(hands["deal_hand"]) == 21:
            end_game(hands)        
        #if computer's hand less than 17, draw again
        elif special_sum(hands["deal_hand"]) <17:
            hands["deal_hand"].append(draw_random())
            round(counter, hands)
        #else - end game
        else:
            end_game(hands)



#--------------------------------
# MAIN FUNCTION STARTS HERE
#--------------------------------
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
both_hands = {
    "my_hand" : [],
    "deal_hand" : []
}

response = input("Do you want to play a game of Blackjack? type 'y' or 'n': ")
if response.lower() == 'n':
    sys.exit("OK, nevermind.")
if response.lower() !='y':
    sys.exit("I'll take it as a No.")

clear()
print(logo)

#round counter
counter = 0 
round(counter, both_hands)


