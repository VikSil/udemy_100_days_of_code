import sys
import os

# import from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import beginner.helper_functions as helper_functions  # all functions that are passed to defensive_while need to return a list with True as first element to break out
from replit import clear


def ask_for_number(sequence: str):
    """
    Asks the user to input a number
    """
    try:
        number = float(input(f"What's the {sequence} number?: "))
        return list([True, number])
    except:
        print("Wrong input. Try again")
        return False


def ask_for_operation():
    """
    Asks the user to choose one of fourpossible operations
    """
    print("+\n-\n*\n/")
    operation = input("Pick an operation: ")
    if operation in ["+", "-", "*", "/"]:
        return list([True, operation])
    else:
        print("Wrong input. Try again")


def calculate(first, operation, second):
    """
    Calculates the result given two operands and an operation
    """
    if operation == "+":
        return float(first) + float(second)
    if operation == "-":
        return float(first) - float(second)
    if operation == "*":
        return float(first) * float(second)
    if operation == "/":
        return float(first) / float(second)


def print_result(first, operation, second, result):
    print(
        f"{str(float(first))} {operation} {str(float(second))} = {str(float(result))}"
    )


def go_again(result):
    """
    Asks the user if they want to use the result for another calculation
    """
    again = input(
        f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation: "
    )
    # if yes - don't stop the calculation loop - False
    if again.lower() == "y":
        return list([True, False])
    # if no - stop the calculation loop - True
    elif again.lower() == "n":
        return list([True, True])
    else:
        print("Wrong input. Try again")


# --------------------------
# MAIN FUNCTION STARTS HERE
# --------------------------
print("This is a calculator app.")

# start a new calculation
need_new_first = True
while True:  # because the calculator never stops by design
    # if start new calculation - ask for first operand
    if need_new_first:
        (first,) = helper_functions.defensive_while(ask_for_number, "first")
    # else -assume that the previous result is the first operand
    else:
        first = result

    # get the operation
    (operation,) = helper_functions.defensive_while(ask_for_operation)
    # get the second operand
    (second,) = helper_functions.defensive_while(ask_for_number, "second")
    # do the calculation
    result = calculate(first, operation, second)
    # tell user the result
    print_result(first, operation, second, result)
    # ask user if they want to start a new calculation
    (need_new_first,) = helper_functions.defensive_while(go_again, result)
    if need_new_first:
        clear()
