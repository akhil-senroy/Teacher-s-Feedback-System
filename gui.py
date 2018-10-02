# "Pynalyze" s/w tool for faculty evaluation by student
# dm 24/03/2017

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from admin import Admin
from start import Start
from student import Student


class MainWindow(Tk):   # main window class for setting up the app
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.option_add("*tearOff", FALSE)  # set tear to false to prevent menu tear offs

        # the common container for all the windows
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky=(N, W, E, S), ipadx=20, ipady=20)
        container.rowconfigure(1, weight=5)
        container.columnconfigure(1, weight=5)

        # the dictionary for all the available frames
        self.frames = {}

        # for loop for setting all the classes into the dictionary
        for F in (Start, Student, Admin):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=(N, W, E, S))

        self.show_frame(Start)  # show the first frame

    def show_frame(self, page_name):
        # '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_remove()  # remove existing windows
        frame = self.frames[page_name]
        frame.grid()  # show the current frame
        frame.winfo_toplevel().geometry("600x350")

    def remove_frame(self):
        for frame in self.frames.values():
            frame.grid_remove()


def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def center():
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 4) - (height // 4)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))


root = MainWindow()


def main():
    # main entire window
    root.title("MCT's RGIT Feedback")
    # root.iconbitmap('icon.png')
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.geometry("600x350")
    root.resizable(width=False, height=False)
    center()
    root.mainloop()


if __name__ == "__main__":
    # call your code here
    main()
