from tkinter import *


window = Tk()
window.title('First GUI program')
window.minsize(width=500, height=300)

label = Label(text="This is a label", font=('Corier New', 24, 'italic'))
label.pack()  # places the element into the window

label['text'] = 'Changed text'
label.config(text='Changed text again')


def button_click():
    button['text'] = 'Clickedy click'
    label['text'] = textbox.get()


button = Button(text='Click Me!', command=button_click)
button.place(x=20, y=35)


textbox = Entry(width=10)
textbox.pack()

# grid system is relative to other components
# it does not work with .pack()
# textbox.grid(column=1, row = 1)


window.mainloop()
