from tkinter import *
from tkinter import ttk


class Start(ttk.Frame):  # the very first frame
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # the menu bar for windows
        menu_bar = Menu(controller)
        controller['menu'] = menu_bar
        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_help = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.add_cascade(menu=menu_edit, label='Edit')
        menu_bar.add_cascade(menu=menu_help, label='Help')

        menu_file.add_command(label='Close', command=self.quit)
        menu_help.add_command(label='About')

        # the label to show info
        label = \
            ttk.Label(self, text="Welcome to MCT's RGIT Feedback !! "
                                 "To start the feedback session make sure to select Student")
        label.grid(row=0, column=0, sticky=(N, W, E))
       

        # option for student or admin
        self.usr = ttk.Combobox(self, state="readonly")
        self.usr['values'] = ('Student', 'Admin')
        self.usr.current(0)
        self.usr.grid(row=1, column=0, padx=10, pady=10, sticky=(N, S))

        filler = ttk.Frame(self, width=200, height=100)
        filler.grid(row=2, column=0)

        # button for starting the next stage
        ttk.Button(self, text="Start", command=lambda: self.select(controller)).\
            grid(row=3, column=0)

        # pad all the elements
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def select(self, controller):
        from student import Student
        from admin import Admin
        if self.usr.get() == 'Student':
            controller.show_frame(Student)
        else:
            controller.show_frame(Admin)
