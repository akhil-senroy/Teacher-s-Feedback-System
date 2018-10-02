from tkinter import *
from tkinter import ttk
from tkinter import messagebox


from start import Start


class Admin(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.admin = StringVar()
        self.password = StringVar()
        self.ip = StringVar()

        lf = ttk.Labelframe(self, text='Admin Login:')

        lf.grid(row=0, column=0, ipadx=10, ipady=10)
        ttk.Label(lf, text="Username  ").grid(row=0, column=0, sticky=(E, W), padx=5, pady=5)
        ttk.Label(lf, text="Password  ").grid(row=1, column=0, sticky=(E, W), padx=5, pady=5)
        ttk.Label(lf, text="Server IP ").grid(row=2, column=0, sticky=W, padx=5, pady=5)

        admin = ttk.Entry(lf, textvariable=self.admin)
        admin.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        admin.focus_set()
        ttk.Entry(lf, textvariable=self.password, show="*").grid(row=1, column=1, sticky=W, padx=5, pady=5)
        ttk.Entry(lf, textvariable=self.ip).grid(row=2, column=1, sticky=W, padx=5, pady=5)

        ttk.Button(self, text="Login", command=lambda: self.adm_check(parent, controller)).\
            grid(row=2, column=2, sticky=E)
        ttk.Button(self, text="< Back", command=lambda: controller.show_frame(Start)). \
            grid(row=2, column=1, sticky=W)

        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def adm_check(self, parent, controller):
        from dbase import DbConnect
        from adminpanel import AdminPanel
        try:
            db_con = DbConnect(self.ip.get())
            c = db_con.db_admin_call(self.admin, self.password)
            ap = AdminPanel(parent, controller, self.ip.get())
            ap.winfo_toplevel().geometry('500x400')
            if c == 1:
                controller.remove_frame()
                ap.grid()
            elif c == 0:
                messagebox.showerror('Pynalyze', 'Please check your user name and password')
                self.password.set("")
            else:
                messagebox.showerror('Pynalyze', 'Multiple administrators are not allowed')
        except DbConnect:
            messagebox.showerror('Pynalyze', 'Server not reachable')
