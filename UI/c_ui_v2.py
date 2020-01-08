# -*- coding: utf-8 -*-
#Consider allowing user to save image of a graph to file

import tkinter as tk
import matplotlib.animation as animation
from matplotlib import use as graph_use
from matplotlib.pyplot import Figure
from time import strftime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Constants import *

def config_frame(mode, start=0, end=1, weighting=1, uniform=''):
    for x in range(start, end): #adjust column/row weighting - less repetitive
        mode(x, weight=weighting, uniform=uniform)

class BioreactorUI(tk.Frame):
    def __init__(self, parent, manager, user, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.manager, self.user = manager, user
        self.init_widgets()
        
    def init_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(0, weight=1)
        self.menu_bar = MenuBar(self, self.manager, self.user,0.1*self.width,
                                self.height, highlightthickness=0, bg=MENU)
        self.menu_options=MenuBtns(self, self.manager, self.user,0.2*self.width,
                                   self.height-20,highlightthickness=0,bg=GREY)
        self.graph_display = GraphFrame(self,0.7*self.width-10,self.height-40,
                                        highlightthickness=1, bg='white',
                                        highlightbackground=MENU,
                                        highlightcolor=MENU)
        for widget in (self.menu_bar, self.menu_options, self.graph_display):
            widget.grid_propagate(0)

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.menu_bar.grid(row=0, column=0, sticky='NEW')
        self.menu_options.grid(row=0, column=1, sticky='NESW')
        self.graph_display.grid(row=0,column=2,sticky='NESW',pady=20,padx=(0,20))
    
class MenuBar(tk.Frame):
    def __init__(self, parent, manager, user, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.manager, self.user = manager, user
        self.init_widgets()
        self.update_time()
        self.update_status()

    def init_widgets(self):
        self.rowconfigure(0, weight=50)
        config_frame(self.rowconfigure, start=1, end=4, weighting=1, uniform='3')
        self.columnconfigure(0, weight=1)
        
        self.lbls = tk.Frame(self,bg=MENU,width=self.width,highlightthickness=0)
        self.lbls.columnconfigure(0, weight=1)
        self.lbls.grid_propagate(0)
        self.watch = tk.Label(self.lbls,font=(FONT, MEDIUM),fg='white',bg=MENU)
        self.status_lbl = tk.Label(self.lbls,font=(FONT,MEDIUM),fg='white',bg=MENU,
                               text='Bioreactor\n[Offline]')
        self.modify_btn = tk.Button(self, text='MODIFY', relief='flat',
                                    font=(FONT_BOLD,MEDIUM),fg='white',bg=GREEN,
                                    activebackground=GREEN,highlightthickness=0,
                                    command=self.manager.open_updater)
        self.logout_btn=tk.Button(self, text='LOGOUT', relief='flat',
                                  font=(FONT_BOLD,MEDIUM), fg='white',bg=YELLOW,
                                  activebackground=YELLOW,highlightthickness=0,
                                  command=self.manager.open_login)
        self.shutdown_btn = tk.Button(self, text='SHUTDOWN', relief='flat',
                                      font=(FONT_BOLD,MEDIUM),fg='white',bg=RED,
                                      activebackground=RED,highlightthickness=0,
                                      command=self.manager.shutdown)
    
    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.lbls.grid(row=0, column=0, sticky='nesw', pady=20, padx=10)
        self.watch.grid(row=0, column=0, sticky='new', pady=(0, 20))
        self.status_lbl.grid(row=1, column=0, sticky='new', pady=(0, 20))
        if self.user == USERNAME and self.manager.connected:
            self.modify_btn.grid(row=1, column=0, sticky='nesw',pady=(0,20),padx=20)
        self.logout_btn.grid(row=2, column=0, sticky='nesw',pady=(0,20),padx=20)
        self.shutdown_btn.grid(row=3,column=0,sticky='nesw',pady=(0,20),padx=20)

    def update_status(self):
        if self.manager.serial is not None: self.status = 'Online'
        else: self.status = 'Offline'
        self.status_lbl.config(text='Bioreactor\n[{}]'.format(self.status))
            
    def update_time(self):
        current_time = strftime('%A\n%H:%M:%S')
        self.watch.config(text=current_time)
        self.parent.after(TIME_DELAY, self.update_time)
        
class MenuBtns(tk.Frame):
    def __init__(self, parent, manager, user, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.manager, self.user = manager, user, 
        self.current_pH, self.current_temp, self.current_speed = 0, 0, 0
        self.init_widgets()
        self.update_lbls()

    def update_lbls(self):
        if self.manager.serial is not None:
            if len(self.manager.vals['pH']) > 0:
                self.current_pH = self.manager.vals['pH'][-1][1]
            else: self.current_pH = 0
            if len(self.manager.vals['temperature']) > 0:
                self.current_temp = self.manager.vals['temperature'][-1][1]
            else: self.current_temp = 0
            if len(self.manager.vals['speed']) > 0:
                self.current_speed = self.manager.vals['speed'][-1][1]
            else: self.current_speed = 0
        else:
            self.current_pH = 0
            self.current_temp = 0
            self.current_speed = 0
        
        self.ph_val.config(text=str(self.current_pH))
        self.temp_val.config(text='{}°C'.format(self.current_temp))
        self.spd_val.config(text='{} RPM'.format(self.current_speed))
    
    def init_widgets(self):
        self.columnconfigure(0, weight=1)
        config_frame(self.rowconfigure, start=0, end=4, weighting=1, uniform='4')
            
        self.info_frame = tk.Frame(self,bg=BLUE,highlightthickness=0)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=3)
        self.info_frame.rowconfigure(1, weight=1)
        self.info_val = tk.Label(self.info_frame, text=self.user, bg=BLUE,
                                 fg='white', font=(FONT_BOLD, LARGE))
        self.info_lbl = tk.Label(self.info_frame, text='Logged in as ↑', bg=BLUE,
                                 fg='white', font=(FONT, FONTSIZE))
        self.info_btn = tk.Button(self.info_frame, bg=BLUE, relief='flat',
                                  activebackground=BLUE)

        self.ph_frame = tk.Frame(self, bg=GREEN, highlightthickness=0)
        self.ph_frame.columnconfigure(0, weight=1)
        self.ph_frame.rowconfigure(0, weight=3)
        self.ph_frame.rowconfigure(1, weight=1)
        self.ph_val = tk.Label(self.ph_frame, text='7', bg=GREEN, fg='white',
                              font=(FONT_BOLD, LARGE))
        self.ph_lbl = tk.Label(self.ph_frame, text='Current pH of Yeast',
                               bg=GREEN, fg='white', font=(FONT, FONTSIZE))
        self.ph_canv = tk.Canvas(self.ph_frame, highlightthickness=0, bg=GREEN)

        self.temp_frame = tk.Frame(self, bg=YELLOW, highlightthickness=0)
        self.temp_frame.columnconfigure(0, weight=1)
        self.temp_frame.rowconfigure(0, weight=3)
        self.temp_frame.rowconfigure(1, weight=1)
        self.temp_val = tk.Label(self.temp_frame, text='32°C',bg=YELLOW,
                                 fg='white', font=(FONT_BOLD, LARGE))
        self.temp_lbl = tk.Label(self.temp_frame, text='Current Temperature',
                                 bg=YELLOW, fg='white', font=(FONT, FONTSIZE))
        self.temp_canv = tk.Canvas(self.temp_frame, highlightthickness=0,
                                   bg=YELLOW)
        
        self.spd_frame = tk.Frame(self, bg=RED, highlightthickness=0)
        self.spd_frame.columnconfigure(0, weight=1)
        self.spd_frame.rowconfigure(0, weight=3)
        self.spd_frame.rowconfigure(1, weight=1)
        self.spd_val = tk.Label(self.spd_frame, text='1500 RPM', bg=RED,
                                fg='white', font=(FONT_BOLD, LARGE))
        self.spd_lbl = tk.Label(self.spd_frame, text='Current Stirring Speed',
                                bg=RED, fg='white', font=(FONT, FONTSIZE))  
        self.spd_canv = tk.Canvas(self.spd_frame, highlightthickness=0, bg=RED)

        self.ph_canv.bind("<Button-1>", lambda event, title='pH of yeast',
                          y_axis='pH', colour=GREEN,btn=self.ph_canv,graph='pH':
                          self.manager.change_graph(title, y_axis, colour,
                                                    btn,  graph, event))
        self.temp_canv.bind("<Button-1>",lambda event, title='Temperature of yeast',
                            y_axis='Temperature (°C)', colour=YELLOW,
                            btn=self.temp_canv, graph='temperature':
                            self.manager.change_graph(title, y_axis, colour,
                                                      btn, graph, event))
        self.spd_canv.bind("<Button-1>", lambda event, title='Stirring Speed',
                           y_axis='Stirring Speed (RPM)', colour=RED,
                           btn=self.spd_canv, graph='speed':
                           self.manager.change_graph(title, y_axis, colour,
                                                     btn, graph, event))
                           
        for widget in self.winfo_children():
            widget.grid_propagate(0)

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.info_frame.grid(row=0, column=0, sticky='nesw',pady=(20,0),padx=20)
        self.info_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=10)
        self.info_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.info_btn.grid(row=0, column=0,columnspan=2,rowspan=2,sticky='nesw')
        self.info_btn.lower()
        
        self.ph_frame.grid(row=1, column=0, sticky='nesw', pady=(20,0), padx=20)
        self.ph_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=10)
        self.ph_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.ph_canv.grid(row=0, column=0, columnspan=2,rowspan=2,sticky='nesw')
        self.ph_val.lift()
        self.ph_lbl.lift()
        
        self.temp_frame.grid(row=2, column=0, sticky='nesw',pady=(20,0),padx=20)
        self.temp_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=10)
        self.temp_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.temp_canv.grid(row=0,column=0,columnspan=2,rowspan=2,sticky='nesw')
        self.temp_val.lift()
        self.temp_lbl.lift()
        
        self.spd_frame.grid(row=3, column=0, sticky='nesw', pady=20, padx=20)
        self.spd_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=5)
        self.spd_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.spd_canv.grid(row=0,column=0,columnspan=2,rowspan=2,sticky='nesw')
        self.spd_val.lift()
        self.spd_lbl.lift()

class GraphFrame(tk.Frame):
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width,self.height,self.body=parent,width,height,None
        self.xs, self.ys = [], []
        self.graph_title, self.graph_colour, self.y_axis = '', RED, ''
        graph_use("TkAgg")
        self.init_widgets()
        
    def init_widgets(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

        self.title_tab = tk.Label(self, bg='white', font=(FONT, LARGE))
        txt=('Either select a value to display on the left '+
             'or it may be the case that the MSP432 board is not connected.')
        self.body = tk.Message(self, bg='white', text=txt, font=(FONT, MEDIUM),
                             anchor='center',highlightthickness=0,justify='left',
                               width=self.width-20)
        
    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.title_tab.grid(row=0, column=0, sticky='esw',padx=10, pady=(10,0))

    def default_screen(self):
        self.title_tab.config(text='No data to display!', fg='black')
        self.body.grid(row=1, column=0, sticky='new', padx=10, pady=10)
        self.parent.update()
        
    def setup_graph(self):
        self.figure = Figure()
        self.graph_plot = self.figure.add_subplot(1, 1, 1)
        self.graph_canvas = FigureCanvasTkAgg(self.figure, self)
        self.graph_canvas.get_tk_widget().grid(row=1, column=0, sticky='nesw',
                                               padx=10)
        
    def run_animation(self):
        self.anim = animation.FuncAnimation(self.figure, self.plot_graph,
                                            interval=FREQUENCY, frames=FRAMES)
        self.graph_canvas.draw()
        self.parent.update()
        
    def plot_optimal_vals(self, graph, subplot, colour=RED):
        min_val, max_val = OPTIMAL_VALS[self.graph_title]
        self.graph_plot.axhline(y=min_val,color=self.graph_colour,linestyle='--')
        self.graph_plot.axhline(y=max_val,color=self.graph_colour,linestyle='--')

    def update_graph_axes(self):
        self.title_tab.config(text='Graph of {} against time'.format(self.graph_title),
                              fg=self.graph_colour)
        self.graph_plot.set_xlabel('Time (seconds)',fontsize=FONTSIZE,
                                   color=self.graph_colour,
                                   horizontalalignment='center', fontname=FONT)
        self.graph_plot.set_ylabel(self.y_axis, fontsize=FONTSIZE,
                                   color=self.graph_colour,
                                   verticalalignment='center', fontname=FONT)
        self.graph_plot.tick_params(color=MENU, labelcolor=MENU)
        for spine in self.graph_plot.spines.values():
            spine.set_edgecolor(MENU)

    def plot_graph(self, i):
     #   self.parent.after(100) - should reduce CPU usage
        self.graph_plot.clear()
        self.update_graph_axes()
        self.graph_plot.plot(self.xs, self.ys, color=self.graph_colour)
        self.plot_optimal_vals(self.graph_title,self.graph_plot,self.graph_colour)
        self.graph_canvas.draw()
