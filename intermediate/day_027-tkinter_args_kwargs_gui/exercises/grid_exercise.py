from tkinter import Tk, Label, Button, Entry


window = Tk()
window.title('First GUI program')
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

label = Label(text="This is a label", font=('Corier New', 24, 'italic'))
label.grid(column=0, row=0)


def button_click():
    new_button['text'] = 'They never listen.'
    label['text'] = textbox.get()


new_button = Button(text='Do not click Me!', command=button_click)
new_button.grid(column=2, row=0)
new_button.config(padx=50, pady=50)


def button_click():
    button['text'] = 'Clickedy click'
    label['text'] = textbox.get()


button = Button(text='Click Me!', command=button_click)
button.grid(column=1, row=1)


textbox = Entry(width=10)
textbox.grid(column=3, row=3)


window.mainloop()
