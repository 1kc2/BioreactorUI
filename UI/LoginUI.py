import tkinter as tk
from Constants import *
    
class LoginMenu(tk.Frame):
    def __init__(self, parent, manager, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.manager = manager
        self.init_widgets()
        self.bind_keys()

    def init_widgets(self):
        #add a background?
        self.grid_propagate(0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.widgets=tk.Frame(self,width=0.5*self.width,height=0.5*self.height,
                              bg=MENU, highlightthickness=1,
                              highlightbackground=BLUE)
        self.widgets.grid_propagate(0)
        for x in range(2):
            self.widgets.columnconfigure(x, weight=1)
        self.title = tk.Label(self.widgets, text='Bioreactor Control System',
                              font=(FONT_BOLD, LARGE), fg='white', bg=MENU)
        txt = ('Please log into an admin account or continue as a guest\nto view'+
               ' the state of the bioreactor.')
        self.body = tk.Label(self.widgets, text=txt, font=(FONT, FONTSIZE),
                             fg='white', bg=MENU)

        self.user_entry = tk.Entry(self.widgets, bg='white', fg='Black',
                                   font=(FONT, FONTSIZE), relief='flat')
        self.user_entry.insert(0, 'Username...')
        self.pass_entry = tk.Entry(self.widgets, bg='white', fg='Black',
                                   font=(FONT, FONTSIZE), relief='flat',
                                   show='*')
        self.pass_entry.insert(0, 'Password...')

        self.login_btn = tk.Button(self.widgets, text='LOGIN', fg='white',
                                   bg=GREEN, font=(FONT, MEDIUM), relief='flat',
                                   highlightthickness=0,
                                   command=self.manager.check_login)
        self.guest_btn = tk.Button(self.widgets, text='GUEST', fg='white',
                                   bg=RED, font=(FONT, MEDIUM), relief='flat',
                                   highlightthickness=0,
                                   command=self.manager.open_dashboard)

    def bind_keys(self):
        for entry in (self.user_entry, self.pass_entry):
            entry.bind('<1>', self.delete_text)
            entry.bind('<Return>', lambda event:self.manager.check_login(event))
        self.widgets.bind('<Return>',lambda event:self.manager.check_login(event))
        self.bind('<Return>', lambda event: self.manager.check_login(event))
        self.user_entry.focus_set()

    def delete_text(self, event):
        if event.widget.get() in ('Username...', 'Password...',):
            event.widget.delete(0, 'end')
        
    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.widgets.grid(row=0, column=0)
        self.title.grid(row=1, column=0, columnspan=2,sticky='nesw',pady=(30,0))
        self.body.grid(row=2, column=0, columnspan=2, sticky='nesw')
        self.user_entry.grid(row=3, column=0, columnspan=2, sticky='nesw',
                             pady=(20, 0), padx=40, ipady=10)
        self.pass_entry.grid(row=4, column=0, columnspan=2, sticky='nesw',
                             pady=(20, 0), padx=40, ipady=10)
        self.login_btn.grid(row=5, column=0, sticky='nesw',padx=(40,20),pady=20,
                            ipady=15)
        self.guest_btn.grid(row=5, column=1, sticky='nesw', padx=(0,40),pady=20,
                            ipady=15)
