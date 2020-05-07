from tkinter import *
import os
import sys
window = Tk()

window.title('Playlist App')
window.geometry('700x400')

lbl = Label(window, text='Customize a new Spotify playlist with just a few inputs!',
            font=('Times New Roman', 20))
lbl.grid(column=0, row=0)


def clicked():
    lbl.configure(text='Button clicked')
    os.system('python bot.py')


btn = Button(window, text="Click to get started", command=clicked)
btn.grid(column=0, row=1)
window.mainloop()
