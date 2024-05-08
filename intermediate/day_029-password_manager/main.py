import os
import json
import pyperclip
from tkinter import *
from tkinter import messagebox  # this is a module not a class, hence needs to be imported separately
from random import choice, randint, shuffle

current_dir = os.path.dirname(os.path.realpath(__file__))


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate():
    letters = [
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = ''.join(password_list)

    password_textbox.delete(0, END)
    password_textbox.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    global current_dir
    website = website_textbox.get()
    username = email_textbox.get()
    psw = password_textbox.get()
    screen_data = {website: {'email': username, 'password': psw}}

    if len(website) == 0 or len(username) == 0 or len(psw) == 0:
        messagebox.showwarning(title='Missing info', message='Please fill out all of the fields.')

    else:
        try:
            with open(f'{current_dir}/output.json', mode='r') as file:
                data = json.load(file)
                data.update(screen_data)

        except FileNotFoundError:
            with open(f'{current_dir}/output.json', mode='w') as file:
                json.dump(screen_data, file, indent=4)

        else:
            with open(f'{current_dir}/output.json', mode='w') as file:
                json.dump(data, file, indent=4)

            website_textbox.delete(0, END)
            password_textbox.delete(0, END)


# ---------------------------- SEARCH FILE ------------------------------- #


def search():

    try:
        with open(f'{current_dir}/output.json') as file:
            file_data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='Credentials Not Found!')
    else:
        search_website = website_textbox.get()
        try:
            found_username = file_data[search_website]['email']
            found_psw = file_data[search_website]['password']
        except KeyError:
            messagebox.showerror(title='Error', message='Credentials Not Found!')
        else:
            messagebox.showinfo(
                title=f'{search_website} credentials', message=f'Username: {found_username}\nPassword: {found_psw}'
            )


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=40, pady=40)

image_path = f'{current_dir}/logo.png'
logo_img = PhotoImage(file=image_path)
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, columnspan=2, sticky='w')


website_label = Label(text='Website:')
website_label.grid(column=0, row=1)


email_label = Label(text='Email/Username:')
email_label.grid(column=0, row=2)


password_label = Label(text='Password:')
password_label.grid(column=0, row=3)


website_textbox = Entry(width=25)
website_textbox.grid(column=1, row=1, sticky='w')
website_textbox.focus()

search_btn = Button(text='Search', width=15, command=search)
search_btn.grid(column=2, row=1, sticky='e')

email_textbox = Entry(width=45)
email_textbox.grid(column=1, row=2, columnspan=2)
email_textbox.insert(END, "myemail@domain.com")

password_textbox = Entry(width=25)
password_textbox.grid(column=1, row=3, sticky='w')

generate_btn = Button(text='Generate Password', command=generate)
generate_btn.grid(column=2, row=3, sticky='e')

save_btn = Button(text='Save', command=save, width=38)
save_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()
