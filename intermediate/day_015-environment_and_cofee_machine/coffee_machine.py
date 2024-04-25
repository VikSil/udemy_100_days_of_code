from global_variables import *


def print_report():
    print(f'Water: {resources["water"]}ml')
    print(f'Milk: {resources["milk"]}ml')
    print(f'Coffee: {resources["coffee"]}g')
    print(f'Money: ${resources["money"]}')


def ask_for_coins(coins_name: str):
    qty = -1
    while qty < 0:
        try:
            qty = int(input(f'How many {coins_name}?: '))
            if qty < 0:
                print('Wrong input. Try again!')
        except ValueError as e:
            print('Wrong input. Try again!')
            qty = -1

    return qty


def accept_coins():
    q = ask_for_coins('quarters')
    d = ask_for_coins('dimes')
    n = ask_for_coins('nickels')
    p = ask_for_coins('pennies')
    payment = p * 0.01 + n * 0.05 + d * 0.1 + q * 0.25
    return payment


def can_make_drink(order: str):
    if MENU[order]['ingredients']['water'] > resources['water']:
        print("Sorry there is not enough water.")
        return False
    elif MENU[order]['ingredients']['coffee'] > resources['coffee']:
        print("Sorry there is not enough coffee.")
        return False
    elif order != 'espresso':
        if MENU[order]['ingredients']['milk'] > resources['milk']:
            print("Sorry there is not enough milk.")
            return False
    return True


def make_drink(order: str):
    resources['water'] -= MENU[order]['ingredients']['water']
    resources['coffee'] -= MENU[order]['ingredients']['coffee']
    if order != 'espresso':
        resources['milk'] -= MENU[order]['ingredients']['milk']


def main():
    resources['money'] = 0

    is_on = True
    while is_on:
        order = None
        while not order:
            order = input('What would you like? (espresso/latte/cappuccino): ')
            if order not in ['espresso', 'latte', 'cappuccino', 'report', 'off']:
                order = None
                print('Wrong input. Try again!')

        if order == 'off':
            is_on = False
        elif order == 'report':
            print_report()
        else:
            if can_make_drink(order):
                print('Please insert coins.')
                payment = accept_coins()
                if payment > MENU[order]['cost']:
                    make_drink(order)
                    print(f"Here is ${round((payment - MENU[order]['cost']),2)} in change.")
                    print(f"Here is your {order} ☕ Enjoy!")
                    resources['money'] += MENU[order]['cost']
                else:
                    print("Sorry that's not enough money. Money refunded.")


if __name__ == "__main__":
    main()
