# -*- coding: utf-8 -*-
import tkinter as tk
from Constants import *
from operator import add, sub
import Utilities

class UpdaterUI(tk.Frame):
    def __init__(self, parent, reactor, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.reactor, self.width = parent, reactor, width
        self.speed = self.reactor.speed
        self.ph = self.reactor.ph
        self.temperature = self.reactor.temperature
        self.mappings = {'+': add, '-': sub}
        self.vals = {'ph': self.ph, 'temperature':self.temperature,
                     'speed':self.speed}
        self.init_widgets()
        self.update_lbls()

    def init_widgets(self):
        self.grid_propagate(0)
        for col in range(3):
            self.columnconfigure(col, weight=1, uniform='3')
        self.rowconfigure(1, weight=1)

        msg = ('Use the up and down arrows to adjust the operation of the ' +
               'bioreactor for each subsystem. Changes are saved on exit.')
        self.info_lbl = tk.Message(self, text=msg, font=(FONT, FONTSIZE),
                                   bg='white', fg='black', width=self.width,
                                   justify='center')
        
        self.ph_frame = tk.Frame(self, bg=GREY, highlightthickness=0)
        self.ph_frame.columnconfigure(0, weight=1)
        for row in range(1,4):
            self.ph_frame.rowconfigure(row, weight=1)
        self.ph_title = tk.Label(self.ph_frame, text='pH',
                                   font=(FONT, FONTSIZE), bg=MENU, fg='white')
        self.ph_up = tk.Button(self.ph_frame, text='▲', font=(FONT, LARGE),
                                 relief='flat', fg=GREEN, bg=GREY)
        self.ph_lbl=tk.Label(self.ph_frame,text=self.ph,
                               font=(FONT, FONTSIZE), bg=GREY, fg='black')
        self.ph_down = tk.Button(self.ph_frame, text='▼', font=(FONT,LARGE),
                                 relief='flat', fg=GREEN, bg=GREY)
        
        self.temp_frame = tk.Frame(self, bg=GREY, highlightthickness=0)
        self.temp_frame.columnconfigure(0, weight=1)
        for row in range(1,4):
            self.temp_frame.rowconfigure(row, weight=1)
        self.temp_title = tk.Label(self.temp_frame, text='Temperature',
                                   font=(FONT, FONTSIZE), bg=MENU, fg='white')
        self.temp_up = tk.Button(self.temp_frame, text='▲', font=(FONT, LARGE),
                                 relief='flat', fg=YELLOW, bg=GREY)
        self.temp_lbl=tk.Label(self.temp_frame,text='{}°C'.format(self.temperature),
                               font=(FONT, FONTSIZE), bg=GREY, fg='black')
        self.temp_down = tk.Button(self.temp_frame, text='▼', font=(FONT,LARGE),
                                 relief='flat', fg=YELLOW, bg=GREY)

        self.spd_frame = tk.Frame(self, bg=GREY, highlightthickness=0)
        self.spd_frame.columnconfigure(0, weight=1)
        for row in range(1,4):
            self.spd_frame.rowconfigure(row, weight=1)
        self.spd_title = tk.Label(self.spd_frame, text='Motor Speed',
                                   font=(FONT, FONTSIZE), bg=MENU, fg='white')
        self.spd_up = tk.Button(self.spd_frame, text='▲', font=(FONT, LARGE),
                                 relief='flat', fg=RED, bg=GREY)
        self.spd_lbl=tk.Label(self.spd_frame,text='{} RPM'.format(self.speed),
                               font=(FONT, FONTSIZE), bg=GREY, fg='black')
        self.spd_down = tk.Button(self.spd_frame, text='▼', font=(FONT,LARGE),
                                 relief='flat', fg=RED, bg=GREY)

        self.apply_btn = tk.Button(self, text='Apply', font=(FONT, FONTSIZE),
                                    relief='flat', bg=MENU, fg='white',
                                    command=self.close)

        self.ph_up.config(command=lambda btn=self.ph_up,
                          subsystem='ph', sign='+':
                          self.update_var(btn, subsystem, sign))
        self.ph_down.config(command=lambda btn=self.ph_down,
                            subsystem='ph', sign='-':
                            self.update_var(btn, subsystem, sign))

        self.temp_up.config(command=lambda btn=self.temp_up,
                            subsystem='temperature', sign='+':
                            self.update_var(btn, subsystem, sign))
        self.temp_down.config(command=lambda btn=self.temp_down,
                              var=self.temperature,subsystem='temperature',
                              sign='-': self.update_var(btn,subsystem,sign))

        self.spd_up.config(command=lambda btn=self.spd_up, 
                           subsystem='speed', sign='-':
                           self.update_var(btn, subsystem, sign))
        self.spd_down.config(command=lambda btn=self.spd_down,
                             subsystem='speed', sign='-':
                             self.update_var(btn, subsystem, sign))
        
    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.info_lbl.grid(row=0, column=0, columnspan=3, sticky='new')
        
        self.ph_frame.grid(row=1, column=0, sticky='nesw', padx=10, pady=10)
        self.ph_title.grid(row=0, column=0, sticky='new', pady=(0,10), ipady=10)
        self.ph_up.grid(row=1, column=0, sticky='nesw', padx=10)
        self.ph_lbl.grid(row=2, column=0, sticky='nesw', padx=10, pady=10)
        self.ph_down.grid(row=3, column=0, sticky='nesw', padx=10, pady=(0,10))
        
        self.temp_frame.grid(row=1, column=1, sticky='nesw', padx=10, pady=10)
        self.temp_title.grid(row=0, column=0, sticky='new',pady=(0,10), ipady=10)
        self.temp_up.grid(row=1, column=0, sticky='nesw', padx=10)
        self.temp_lbl.grid(row=2, column=0, sticky='nesw', padx=10, pady=10)
        self.temp_down.grid(row=3, column=0, sticky='nesw', padx=10, pady=(0,10))

        self.spd_frame.grid(row=1, column=2, sticky='nesw', padx=10, pady=10)
        self.spd_title.grid(row=0, column=0, sticky='new',  pady=(0,10), ipady=10)
        self.spd_up.grid(row=1, column=0, sticky='nesw', padx=10)
        self.spd_lbl.grid(row=2, column=0, sticky='nesw', padx=10, pady=10)
        self.spd_down.grid(row=3, column=0, sticky='nesw', padx=10, pady=(0,10))

        self.apply_btn.grid(row=2, column=0, columnspan=3, sticky='nesw',
                             padx=10, pady=(0,10))

    def enable_btns(self):
        btns = [self.ph_up, self.ph_down, self.temp_up, self.temp_down,
                self.spd_up, self.spd_down]
        for button in btns:
            button.config(state='normal')
            
    def check_vals(self, btn, var, subsystem, sign):
        self.enable_btns()
        min_val, max_val, increment = VAL_RANGES[subsystem]
        new_value = self.mappings[sign](var, increment)
        if min_val <= new_value <= max_val:
            btn.config(state='normal')
            return new_value, True
        else:
            btn.config(state='disabled')
            return -1, False
        
    def update_var(self, btn, subsystem, sign):
        new_value, valid=self.check_vals(btn,self.vals[subsystem],subsystem,sign)
        if valid:
            self.vals[subsystem] = new_value
            self.ph = self.vals['ph']
            self.temperature = self.vals['temperature']
            self.speed = self.vals['speed']
            self.update_lbls()
        
    def update_lbls(self):
        self.ph_lbl.config(text=str(self.ph))
        self.temp_lbl.config(text='{}°C'.format(self.temperature))
        self.spd_lbl.config(text='{} RPM'.format(self.speed))

    def confirm_updates(self):
        self.reactor.speed = self.speed
        self.reactor.ph = self.ph
        self.reactor.temperature = self.temperature
        msgs_sent = self.reactor.update()
        if not msgs_sent:
            Utilities.error_msg('Connection error', 'No board to send data to.')
        
    def close(self):
        self.confirm_updates()
        self.parent.quit()
        self.parent.destroy()  
