from tkinter import Tk, Label, Button, Entry


window = Tk()
window.minsize(width=250, height=100)
window.title('Miles to Km Converter')
window.config(padx=20, pady=20)

miles_textbox = Entry(width=10)
miles_textbox.grid(column=1, row=0)

miles_label = Label(text='Miles', font=('Corier New', 15, 'italic'))
miles_label.grid(column=2, row=0)
miles_label.config(padx=5, pady=3)

equal_label = Label(text='is equal to', font=('Corier New', 15, 'italic'))
equal_label.grid(column=0, row=1)

calc_label = Label(text='', font=('Corier New', 15, 'italic'))
calc_label.grid(column=1, row=1)

km_label = Label(text='Km', font=('Corier New', 15, 'italic'))
km_label.grid(column=2, row=1)


def button_click():
    try:
        miles = float(miles_textbox.get())
    except ValueError as e:
        miles = 0
    km = round(miles * 1.6, 2)
    calc_label['text'] = str(km)


button = Button(text='Calculate', command=button_click)
button.grid(column=1, row=2)

window.mainloop()
