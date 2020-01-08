import tkinter as tk
from Constants import *

def error_msg(title='', msg=''): #try, except needed when user closes window
    #before closing the messagebox
    try: tk.messagebox.showerror(title, msg)
    except tk.TclError: return

def centralise(win):
    win.update_idletasks() 
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
def truncate(array):
    if len(array) == MAX_DATA_POINTS:
        del array[0]
    return array
