import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class StudentForm(ttk.Frame):
    def __init__(self, parent, controller, host):
        ttk.Frame.__init__(self, parent)

        self.controller = controller

        self.div = StringVar()
        self.sem = StringVar()
        self.t = StringVar()
        self.tent = []
        self.ip = host
        self.ent = []
        self.block = BooleanVar(self, FALSE)
        self.count = 1
        self.inc = 0
        self.dept = None
        self.current_tid = None
        self.batch = None
        self.review = []
        self.rb = []

        # frame for teacher's list
        # variable to store questions
        self.q = StringVar()
        self.top_lvl = None
        # ttk.Frame(self, width=400).grid(row=0, column=0)
        q_box = ttk.Frame(self, height=50, width=300)
        q_box.grid(row=1, column=1, sticky=(W, E))
        q_box.grid_propagate(0)

        question = Message(q_box, textvariable=self.q, width=300)
        question.grid(row=1, column=1, sticky=(W, E))

        # frame for radio buttons

        self.marks = IntVar()
        self.answers = ["Excellent", "Very Good", "Good", "Needs Improvement", "Unsatisfactory"]

        # radio buttons for the grading
        self.rb_init(self)

        '''rb1 = ttk.Radiobutton(r_frame, text=self.answers[0], variable=self.marks, value=5)
        rb1.grid(row=0, column=0, sticky=W)
        rb2 = ttk.Radiobutton(r_frame, text=self.answers[1], variable=self.marks, value=4)
        rb2.grid(row=1, column=0, sticky=W)
        rb3 = ttk.Radiobutton(r_frame, text=self.answers[2], variable=self.marks, value=3)
        rb3.grid(row=2, column=0, sticky=W)
        rb4 = ttk.Radiobutton(r_frame, text=self.answers[3], variable=self.marks, value=2)
        rb4.grid(row=3, column=0, sticky=W)
        rb5 = ttk.Radiobutton(r_frame, text=self.answers[4], variable=self.marks, value=1)
        rb5.grid(row=4, column=0, sticky=W)'''

        confirm_btn = ttk.Button(self, text="Confirm >", command=lambda: self.eval_quest(self.count))
        confirm_btn.grid(row=3, column=1, sticky=E, padx=10)

        self.question_loop()

        # confirm_btn.bind('<Return>', lambda: self.eval_quest(self.count))

        for child in self.winfo_children():
            child.grid_configure(padx=6, pady=6)

    def rb_init(self, root):
        r_frame = ttk.Frame(root, borderwidth=5, relief=GROOVE, width=50)
        r_frame.grid(row=2, column=1, sticky=W)
        for r in range(5):
            self.rb.append(ttk.Radiobutton(r_frame, text=self.answers[r], variable=self.marks, value=5-r))
            self.rb[r].grid(row=r, column=0, sticky=W)

    def eval_quest(self, i):
        from dbase import DbConnect
        db = DbConnect(self.ip)
        stmt = 'select t_id,t_sub from teacher where dept="' + str(self.dept) + '" and t_div="' + str(
            self.div) + '" and sem=' + str(self.sem)
        # print(stmt)
        db.cu.execute(stmt)
        res = db.cu.rowcount
        if res != 0:
            res += db.cu.execute('select t_id,t_sub from practical where dept=%s and batch=%s and sem=%s',
                                 (str(self.dept), self.batch, str(self.sem)))
            if self.inc <= res:
                if self.marks.get() != 0:
                    db.cu.execute('select * from mt_question')
                    q_count = db.cu.rowcount
                    if i <= q_count:
                        self.eval()
                        self.question_loop()
                    else:
                        self.eval()
                        self.tent.append(self.ent)
                        # print("inputs "+str(len(self.tent)))
                        self.ent = []
                        self.count = 1
                        self.question_loop()
                        # print("i am here")
                        self.text_rev()
                        # self.show_teacher()
                else:
                    messagebox.showwarning('Pynalyze', 'Select an option')
        else:
            messagebox.showerror("MCT's RGIT", "Teachers for the student does not exists")

    def question_loop(self):
        from dbase import DbConnect

        db = DbConnect(self.ip)
        # db.cu.execute('select i from con')
        # row = db.cu.fetchone()
        # if row[0]:
        db.cu.execute('select q_text,q_options from mt_question where q_id='+str(self.count))
        res = db.cu.fetchone()
        self.q.set(str(self.count)+"."+res[0])
        self.count += 1
        opt = res[1].split(',')
        for r in range(5):
            self.rb[r].config(text=opt[r])
        # else:
        #    db.cu.execute('select q_text from mt_question where q_id='+str(33+self.count)+'')
        #    res = db.cu.fetchone()
        #    self.count += 1
        #    try:
        #       self.q.set(res[0])
        #   except self.q:
        #       self.show_teacher()

    def eval(self):
        self.ent.append(self.marks.get())
        self.marks.set(0)

    def set_var(self, dept, sem, div, batch):
        self.dept = dept
        self.sem = sem
        self.div = div
        self.batch = batch
        self.show_teacher()

    def show_teacher(self):
        from dbase import DbConnect
        self.inc += 1

        top_list = ttk.Frame(self, height=200, width=160, borderwidth=2, relief=GROOVE)
        top_list.grid(row=0, column=0, rowspan=3, sticky=(N, W), padx=6, pady=6, ipadx=5, ipady=5)
        top_list.grid_propagate(0)

        db = DbConnect(self.ip)
        stmt = 'select t_id,t_sub from teacher where dept="'+str(self.dept)+'" and t_div="'+str(self.div)+'" and sem='\
               + str(self.sem)
        db.cu.execute(stmt)
        res = db.cu.fetchall()
        name = []
        sub = []
        tid_list = []
        # print(res)
        for t in res:
            db.cu.execute('select t_name from mt_teacher where t_id='+str(t[0]))
            # print(str(t[0]))
            row = db.cu.fetchall()
            name.append(row[0])
            sub.append(t[1])
            tid_list.append(t[0])
        stmt = "select t_id,t_sub from practical where dept=%s and batch=%s and sem=%s"
        batch_data = (str(self.dept), self.batch, str(self.sem))
        db.cu.execute(stmt, batch_data)
        bat = db.cu.fetchone()
        res = res+(bat,)
        if bat is not None:
            db.cu.execute('select t_name from mt_teacher where t_id='+str(bat[0]))
            bat_t = db.cu.fetchall()
            name.append(bat_t[0])
            sub.append(bat[1])
            tid_list.append(bat[0])
        for t in name:
            ttk.Label(top_list, text=t).grid(padx=6, pady=6)
        info = ttk.Frame(self, height=100, width=400, borderwidth=2, relief=GROOVE)
        info.grid(row=0, column=1, columnspan=3, sticky=(N, W), padx=6, pady=6)
        try:
            n = ''.join(name[self.inc-1])
            self.current_tid = tid_list[self.inc-1]
            s = ''.join(sub[self.inc-1])
            self.t.set('Name:   '+n+'      Dept:  '+str(self.dept)+'      Subject:  '+s)
            ttk.Label(info, textvariable=self.t).grid(row=0, column=0, ipadx=25, ipady=20, sticky=E)
        except IndexError:
            self.grid_remove()
            # update to database
            time_input = datetime.date.today().strftime("%B %Y")
            k = -1
            stmt = 'select count(q_id) from mt_question'
            db.cu.execute(stmt)
            c = db.cu.fetchone()
            db.cu.execute('lock tables feedback write, teacher_review write')
            for t in res:
                k += 1
                count_review = 0
                # print(self.review)
                '''if k < len(self.review):
                    if len(self.review[k]) != 0:
                        stmt = ("INSERT INTO teacher_review "
                                "(t_id, review, time) "
                                "values (%s, %s, %s);")
                        data = (t[0], self.review[k], time_input)
                        # print(data)
                        stmt = ("INSERT INTO teacher_review "
                                "(t_id, review, time, t_sub, t_div) "
                                "values (%s, %s, %s, %s, %s);")
                        print(s)
                        data = (t[0], self.review[k], time_input, s, self.div)
                        db.cu.execute(stmt, data)'''
                for i in range(c[0]):
                    # stmt = ("INSERT INTO feedback "
                    #        "(t_id, q_id, time) "
                    #        "values (%s, %s, %s);")
                    # data = (t[0], i+1, time_input)
                    # db.cu.execute(stmt, data)
                    # db.db.commit()
                    for j in range(len(self.tent)):
                        # stmt = "update feedback " \
                        #        "set `%s` = `%s` + 1 " \
                        #        "where t_id=%s and q_id=%s and time=%s ; "
                        stmt = ('update feedback '
                                'set `%s` = `%s` + 1 '
                                'where t_id=%s and q_id=%s and time=%s and t_sub=%s and (t_div=%s or t_div=%s);')
                        if j == k:
                            # print("normal")
                            # data = (self.tent[j][i], self.tent[j][i], t[0], i+1, time_input)
                            data = (self.tent[j][i], self.tent[j][i], t[0], i+1, time_input, sub[j],
                                    str(self.div), self.batch)
                            db.cu.execute(stmt, data)
                            if count_review == 0:
                                if k < len(self.review):
                                    if len(self.review[k]) != 0:
                                        '''stmt = ("INSERT INTO teacher_review "
                                                "(t_id, review, time) "
                                                "values (%s, %s, %s);")
                                        data = (t[0], self.review[k], time_input)'''
                                        # print(data)
                                        stmt = ("INSERT INTO teacher_review "
                                                "(t_id, review, time, t_sub, t_div) "
                                                "values (%s, %s, %s, %s, %s);")
                                        print(sub[j])
                                        data = (t[0], self.review[k], time_input, sub[j], self.div)
                                        db.cu.execute(stmt, data)
                    count_review = 1
            messagebox.showinfo('Pynalyze', 'Thank You')
            self.controller.destroy()
            db.db.commit()
            db.cu.execute('unlock tables')

    def text_rev(self):
        # self.grab_set()

        self.top_lvl = Toplevel(self)
        self.top_lvl.lift()
        self.top_lvl.focus()
        self.top_lvl.grab_set()
        label1 = ttk.Label(self.top_lvl, text="Remarks If Any : ")
        label1.grid(row=0, column=0, ipadx=10, ipady=10, padx=10, pady=5)
        remark = Text(self.top_lvl, height=5, width=50)
        remark.grid(row=0, column=1, padx=10, pady=10)
        self.top_lvl.protocol("WM_DELETE_WINDOW", self.on_close)
        submit_rev = ttk.Button(self.top_lvl, text="Submit",
                                command=lambda: self.submit_rev(remark.get("1.0", "end-1c")))
        submit_rev.grid(row=1, column=2, ipadx=5, ipady=5, padx=10, pady=10)

    def on_close(self):
        messagebox.showinfo("Pynalyze", "New Teacher")
        self.review.append('')
        self.top_lvl.destroy()
        self.show_teacher()

    def submit_rev(self, rev):
        self.review.append(rev)
        self.submit_close()

    def submit_close(self):
        messagebox.showinfo("Pynalyze", "New Teacher")
        self.top_lvl.destroy()
        self.show_teacher()
