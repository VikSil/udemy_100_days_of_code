

def defensive_while(function):
    keep_looping = True
    while keep_looping:
        if function() == False:
            keep_looping = False


def ask_for_input():
    global funct
    funct = input("Type 'encode' to encrypt, type 'decode' to decrypt: ")
    if funct.lower() == 'encode' or funct.lower() == 'decode':
        return False
    else:
        print("Invalid input. Try again.")


def ask_for_message():
    global message
    message = input("Type your message without spaces, use letters only.\n")
    for char in message:
        if char not in letters:
            print("Invalid input. Try again.")
            return True
    return False

def ask_for_shift():
    global shift
    try:
        shift = int(input("Type the shift number.\n"))
        if shift == 0 or shift % 26 == 0:
            print("Invalid input. Try again.")
        elif shift >25:
            shift =  shift % 26
            return False
        else:
            return False
    except:
        print("Invalid input. Try again.")

def encrypt(message:str, shift:int, direction:int):
    new_msg = ''
    for char in message:
        global letters
        position = letters.index(char)
        new_position = position + shift*direction
        length = len(letters)-1
        if new_position > length:
            new_position = new_position - length - 1
        new_msg += letters[new_position]
    print(f"Here is the encoded result: {new_msg}")



letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
funct = ''
message = ''
shift = 0

go_on = True
while go_on:
#ask user if they want to encrypt or decrypt
    defensive_while(ask_for_input)
    defensive_while(ask_for_message)    
    defensive_while(ask_for_shift)
    if funct.lower() == 'encode':
        direction = 1
    else:
        direction = -1

    encrypt(message, shift, direction)


    print()
    go_again = input("Type 'Stop' if you want to exit the program. Otherwise, let's go again!\n")
    if go_again.lower() == "stop":
        go_on = False