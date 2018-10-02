from pymysql import *
import tkinter.messagebox


def function_1():
    db = connect(host="localhost", user="root", passwd="", db="hack")
    var1 = 602
    var2 = 'Sahil'
    cursor = db.cursor()
    cursor.execute("SELECT * from student where rollno=(%s) and name=(%s)", (var1, var2))

    rows = cursor.rowcount
    print(rows)

    if not rows:
        tkinter.messagebox.showinfo("Pynalyze","Invalid User ID and Password Combination!")

    db.commit()

    cursor.close()
    db.close()


function_1()
