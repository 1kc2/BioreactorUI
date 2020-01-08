from Constants import *
from random import randint, choice
import tkinter as tk

class SplashScreen(tk.Frame):
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.init_widgets()

    def init_widgets(self):
        self.grid_propagate(0)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.x1 = self.width//2 - self.width//6.4
        self.y1 = self.height//2 - self.height//3.6
        self.x2 = self.width//2 + self.width//6.4
        self.y2 = self.height//2 + self.height//3.6

        self.canvas = tk.Canvas(self, width=self.width, height=self.height,
                                highlightthickness=0, bg=GREY)

        self.default_coords=[self.width//2-self.width*9/64, self.height//2-self.height//4,
                      self.width//2+self.width*9/64, self.height//2+self.height//4]
        #[self.width//2-self.width*7/64,self.height//2-self.height*7/36,
         #                    self.width//2+self.width*7/64,self.height//2+self.height*7/36]
                  
        self.oval=self.canvas.create_oval(self.default_coords,outline='white',
                                          fill=YELLOW, width=5)
    
        self.outline=self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, 
                                             width=self.height//24,
                                             outline='white')
        self.load_bar=self.canvas.create_arc(self.x1, self.y1, self.x2, self.y2,
                                             width=self.height//36, style='arc',
                                             start=0, extent=0, outline=MENU)
        self.counter = self.canvas.create_text(self.width//2, self.height//2,
                                               text='0% Loaded', fill='white',
                                               font=(FONT, LARGE))

        self.msgs = ['Adjusting pH', 'Initialising stirrer', 'Warming heater',
                     'Calibrating sensors', 'Initialising pins', 'Allocating memory',
                     'Interfacing bioreactor', 'Interfacing bread board',
                     'Establishing connections', 'Initialising pumps',
                     'Calculating optimal levels', 'Powering bioreactor',
                     'Plotting yeast data', 'Retrieving yeast data']
        self.msg_lbl=self.canvas.create_text(self.width//2,
                                             self.height//2+self.height//24,
                                             fill='white',font=(FONT,FONTSIZE))

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.canvas.grid(row=0, column=0, sticky='nesw')

    def animate(self):
        percentage = x = 0
        while percentage < MAX_ANGLE:
            self.parent.after(FRAMES_PER_SECOND)
            percentage = self.update(percentage)
         #   if x % 12 == 0: self.heartbeat()
            x += 1
        self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, width=20,
                                outline=MENU)
        self.canvas.itemconfig(self.msg_lbl,text='> Bioreactor: [Online]',
                               fill='green')
        self.parent.update()
        self.parent.after(DELAY)
        return True

    def heartbeat(self, depth=0):
        new_coords = [self.width//2-self.width*9/64, self.height//2-self.height//4,
                      self.width//2+self.width*9/64, self.height//2+self.height//4]
        if self.canvas.coords(self.oval) == self.default_coords:
            self.canvas.coords(self.oval, new_coords)
        else: self.canvas.coords(self.oval, self.default_coords)
        if depth < 2:
            if depth == 1: delay = FRAMES_PER_SECOND*3
            else: delay = FRAMES_PER_SECOND*12
            self.parent.update()
            self.after(delay)
            self.heartbeat(depth+1)
        self.parent.update()
        
    def update(self, percentage):
        load_addition = randint(1, MAX_INCREMENT+1)
        if load_addition + percentage > MAX_ANGLE: self.update(percentage)
        else: percentage += load_addition
        self.move_bar(percentage)
        return percentage

    def move_bar(self, percentage):
        #try:
        next_msg = choice(self.msgs)
        self.canvas.itemconfig(self.msg_lbl, text=next_msg)
        self.canvas.itemconfig(self.load_bar, extent=-percentage) 
        percent_completed = int(percentage / MAX_ANGLE * 100)
        self.canvas.itemconfig(self.counter,text=str(percent_completed)+'% LOADED')
        self.parent.update()
        #except: pass 
