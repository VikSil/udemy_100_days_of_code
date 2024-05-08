from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


def main():
    machine = CoffeeMaker()
    menu = Menu()
    till = MoneyMachine()

    is_on = True
    while is_on:
        drink = None
        while not drink:
            order = input(f'What would you like?  ({menu.get_items()}): ')
            if order == 'report':
                machine.report()
                till.report()
            elif order == 'off':
                is_on = False
                drink = 'Exit'
            else:
                drink = menu.find_drink(order)

        if is_on and machine.is_resource_sufficient(drink):
            if till.make_payment(drink.cost):
                machine.make_coffee(drink)


if __name__ == "__main__":
    main()
