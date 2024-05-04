import os
import pandas as pd
import random
from tkinter import Tk, Label, Button, PhotoImage, Canvas


BACKGROUND_COLOR = "#B1DDC6"
DISPLAY_TIME = 3000 # in miliseconds
current_dir = os.path.dirname(os.path.realpath(__file__))
dictionary_filepath = f'{current_dir}/data/spanish_english_dictionary.csv'
known_words_filepath = f'{current_dir}/data/known_words.csv'


# ---------------------------- INIT ------------------------------- #

words_df = pd.read_csv(dictionary_filepath)
spanish_words = words_df['spanish'].to_list()
try:
    known_df = pd.read_csv(known_words_filepath)
    known_spanish_words = known_df['spanish'].to_list()
except FileNotFoundError:
    with open(known_words_filepath, mode='w') as file:
        file.write('spanish, english')
        known_spanish_words = []


# ---------------------------- COUNTDOWN -------------------- #

def flip_card():
    global words_df
    x_btn['command'] = x_btn_click
    check_btn.configure(command=check_btn_click)
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(language_label, text='English', fill='white')
    spanish_word = canvas.itemcget(word_label, 'text')
    english_word = words_df.loc[(words_df['spanish'] == spanish_word)].iloc[0]['english']
    canvas.itemconfig(word_label, text=english_word, fill='white')


# ---------------------------- BUTTON COMMANDS -------------------- #

def get_new_word():
    global spanish_words
    global known_spanish_words

    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(language_label, text='Spanish', fill='black')
    got_new_word = False
    while not got_new_word:
        new_word = random.choice(spanish_words)
        if new_word not in known_spanish_words:
            got_new_word = True
    
    canvas.itemconfig(word_label, text=new_word, fill = 'black')
    x_btn.configure(command='do_nothing') 
    check_btn.configure(command='do_nothing')
    window.after(DISPLAY_TIME, flip_card)


def x_btn_click():
    get_new_word()

def check_btn_click():
    global known_spanish_words
    global words_df
    global known_df
    known_word_in_english = canvas.itemcget(word_label, 'text')
    known_translation = words_df[(words_df['english'] == known_word_in_english)]
    known_word_in_spanish = known_translation.iloc[0]['spanish']
    known_spanish_words.append(known_word_in_spanish)
    known_translation.to_csv(known_words_filepath, mode = 'a', index = False, header=False)

    get_new_word()


# ---------------------------- GUI  ------------------------------- #

window = Tk()
window.minsize(width=800, height=526)
window.title('Flash Cards')
window.config(padx=50, pady=50, bg = BACKGROUND_COLOR)


card_front_img = PhotoImage(file = f'{current_dir}/images/card_front.png')
card_back_img = PhotoImage(file = f'{current_dir}/images/card_back.png')
canvas = Canvas(width=800, height=526, highlightthickness=0)
card = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg = BACKGROUND_COLOR)
language_label = canvas.create_text(390, 150, font = ('Ariel', 40, 'italic'))
word_label = canvas.create_text(390, 263,  font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

x_btn_img = PhotoImage(file = f'{current_dir}/images/wrong.png')
x_btn = Button(command=x_btn_click, image=x_btn_img, border=0, highlightthickness=0)
x_btn.grid(column=0, row=1)
check_btn_img = PhotoImage(file = f'{current_dir}/images/right.png')
check_btn = Button(command=check_btn_click, image=check_btn_img, border =0, highlightthickness=0)
check_btn.grid(column=1, row=1)

get_new_word()


window.mainloop()
