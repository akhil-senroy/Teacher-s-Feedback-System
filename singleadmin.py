from MySQLdb import *
import tkinter.messagebox


class SingleAdmin:
    def __init__(self):
        self.db = connect(host="localhost", user="root", passwd="123php!@#", db="pz")
        self.cu = self.db.cursor()

    def db_call(self):
        stmt = "SELECT * from session"
        self.cu.execute(stmt)
        rows = self.cu.fetchall()

        for row in rows:
            for col in row:
                s = col
        print(s)
        if s:
            tkinter.messagebox.showinfo('Pynalyze', 'Cannot Create Multiple Admins')
            return 0
        else:
            print(" Cool!")
            update = "UPDATE session set admin=1 where admin=0"
            self.cu.execute(update)
            self.db.commit()
            return 1

        self.cu.close()
        self.db.close()
