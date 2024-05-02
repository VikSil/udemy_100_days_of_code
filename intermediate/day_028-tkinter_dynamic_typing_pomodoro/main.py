import os
import math

from tkinter import *


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 20
cycles = 0
signal_reset = False

# ---------------------------- TIMER RESET ------------------------------- #


def display_checkmarks():
    checkmarks = ''.join(['✔ '] * math.floor(cycles/2))
    checkmarks_label['text'] = checkmarks

def reset_btn_click():
    global cycles
    global signal_reset
    cycles = 0
    display_checkmarks()
    signal_reset = True

# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_btn_click():
    global cycles
    work_sec = WORK_MINUTES * 60
    short_break_sec = SHORT_BREAK_MINUTES * 60
    long_break_sec = LONG_BREAK_MINUTES * 60

    start_btn['state'] = 'disabled'
    cycles += 1

    if cycles % 2 == 1:
        timer_label.config(text = 'Work!', fg = GREEN)
        countdown(work_sec)
    elif cycles % 8 == 0:
        timer_label.config(text ='Chill', fg = RED)
        display_checkmarks()
        countdown(long_break_sec)
    else:
        timer_label.config(text ='Break', fg = PINK)
        display_checkmarks()
        countdown(short_break_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(num):
    global signal_reset
    if num > 0 and not signal_reset:
        minutes = math.floor(num / 60) 
        seconds = num % 60
        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'

        canvas.itemconfig(timer_text, text=f'{minutes}:{seconds}')
        window.after(1000, countdown, num -1)
    elif signal_reset:
        signal_reset = False
        canvas.itemconfig(timer_text, text='00:00')
        timer_label['text'] = 'Timer'
        start_btn['state'] = 'active'

    else:
        start_btn_click()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Pomodoro Timer')
window.config(padx = 100, pady = 50, bg = YELLOW)


current_dir = os.path.dirname(os.path.realpath(__file__))
image_path = f'{current_dir}/tomato.png'
tomatoe_img = PhotoImage(file = image_path)
canvas = Canvas(width = 200, height = 224, bg = YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomatoe_img)
timer_text = canvas.create_text(100, 130, text = '00:00', fill = 'white', font = (FONT_NAME, 25, 'bold'))
canvas.grid(column=1, row=1)


timer_label = Label(text='Timer', foreground=GREEN, background=YELLOW, font=(FONT_NAME, 25, 'bold'), pady=20)
timer_label.grid(column=1, row=0)

checkmarks_label = Label(text='', foreground=GREEN, background=YELLOW, font=(FONT_NAME, 10, 'bold'), pady=20)
checkmarks_label.grid(column=1, row=3)
display_checkmarks()

start_btn = Button(text='Start', background=YELLOW, command=start_btn_click)
start_btn.grid(column = 0, row =2)

reset_btn = Button(text='Reset',  background=YELLOW, command=reset_btn_click)
reset_btn.grid(column=2, row=2)

window.mainloop()
