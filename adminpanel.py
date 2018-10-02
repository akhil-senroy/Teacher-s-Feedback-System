import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import pymysql as pm


# from tg1 import tg1


class AdminPanel(ttk.Frame):
    def __init__(self, parent, controller, host):
        from dbase import DbConnect
        ttk.Frame.__init__(self, parent)
        menu_bar = Menu(controller)
        controller['menu'] = menu_bar
        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_setting = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.add_cascade(menu=menu_edit, label='Edit')
        menu_setting.add_cascade(menu=menu_edit, label='setting')
        self.percent = DoubleVar()
        self.fb = StringVar()
        self.ip = host
        self.db = DbConnect(self.ip)
        self.teacher_value = []
        self.sp_teacher_value = []

        n = ttk.Notebook(self)
        # general = ttk.Frame(n)  # first page, which would get widgets gridded into it
        tools = ttk.Frame(n)  # second page
        stats = ttk.Frame(n)  # graph page

        graph = ttk.Combobox(stats)
        graph['values'] = ('', 'All teachers')
        graph.current(0)
        graph.grid(row=0, column=0, padx=10, pady=10)
        # ttk.Button(stats, text='Generate graph', command=lambda: tg1(host)).grid(row=0, column=1, padx=10, pady=10)

        mail = ttk.Combobox(stats)
        db = DbConnect(self.ip)
        db.cu.execute('select t_name from mt_teacher')
        row = db.cu.fetchall()
        # print(row)
        mail['values'] = row
        mail.grid(row=1, column=0)
        ttk.Button(stats, text="Send Mail", command=lambda: messagebox.showinfo('Pynalyze', 'Message sent successfully')
                   ).grid(row=1, column=1)

        # sel = ttk.LabelFrame(general, text='Selection')
        # sel.grid(row=0, column=0, padx=10, pady=10)

        # ttk.Label(sel, text='Select Department code').grid(row=0, column=0, padx=10, pady=10, sticky=W)
        # self.dept = ttk.Combobox(sel)
        # self.dept.grid(row=0, column=1, sticky=W)
        # self.db.cu.execute('select distinct s_dept from student')
        # self.dept['values'] = self.db.cu.fetchall()

        # ttk.Entry(sel, textvariable=self.percent).grid(row=1, column=1, sticky=W)
        # ttk.Label(sel, text='Minimum Percentage : ').grid(row=1, column=0, padx=10, pady=10, sticky=W)

        # ttk.Label(sel, text='Select Semester').grid(row=2, column=0, padx=10, pady=10, sticky=W)
        # self.sem = ttk.Combobox(sel)
        # self.sem.grid(row=2, column=1, sticky=W)
        self.db.cu.execute('select distinct s_sem from student')
        # self.sem['values'] = self.db.cu.fetchall()

        # ttk.Label(sel, text='Select Division').grid(row=3, column=0, padx=10, pady=10, sticky=W)
        # self.div = ttk.Combobox(sel)
        # self.div.grid(row=3, column=1, sticky=W)
        # self.db.cu.execute('select distinct s_div from student')
        # self.div['values'] = self.db.cu.fetchall()

        # ttk.Label(sel, text='Type of Feedback').grid(row=4, column=0, padx=10, pady=10, sticky=W)
        # sf = ttk.Frame(sel, borderwidth=2, relief=GROOVE)
        # sf.grid(row=4, column=1, sticky=E)
        # ttk.Radiobutton(sf, variable=self.fb, text='Standard', value='0').grid(row=0, column=0)
        # ttk.Radiobutton(sf, variable=self.fb, text='Behavioral', value='1').grid(row=0, column=1)
        # ttk.Button(sel, text='Start', command=lambda: self.update_all()).grid(row=5, column=2)
        self.db.db.close()
        # n.add(general, text='General')
        n.add(tools, text='Tools')
        n.add(stats, text='Stats')
        n.grid()

        tools_notebook = ttk.Notebook(tools)
        add_user = ttk.Frame(tools_notebook)
        report = ttk.Frame(tools_notebook)
        add_teacher = ttk.Frame(tools_notebook)
        tools_notebook.grid()

        tools_notebook.add(report, text='Report')
        tools_notebook.add(add_teacher, text='Add teacher')
        tools_notebook.add(add_user, text='Add user')

        ttk.Separator(tools).grid(row=3)

        ttk.Button(report, text="Generate Table", command=lambda: self.create_entries()) \
            .grid(row=4, column=0, padx=10, pady=10, sticky=W)

        self.show_report(report)
        self.add_teacher(add_teacher)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def update_all(self):
        from dbase import DbConnect
        db = DbConnect(self.ip)
        db.cu.execute('update con set i='+str(self.fb.get())+' where p=1')
        db.db.commit()
        messagebox.showinfo("Pynalyze", "feedback session  has started")

    def create_entries(self):
        from dbase import DbConnect
        import datetime
        db = DbConnect(self.ip)
        time_input = datetime.date.today().strftime("%B %Y")
        # stmt = 'select t_id from mt_teacher'
        # db.cu.execute(stmt)
        db.cu.execute('select t_id,t_sub,t_div from teacher')
        res = db.cu.fetchall()
        stmt = 'select t_id from feedback where time="'+time_input+'"'
        db.cu.execute(stmt)
        check = db.cu.fetchall()
        stmt = 'select count(q_id) from mt_question'
        db.cu.execute(stmt)
        c = db.cu.fetchone()
        db.cu.execute('select t_id, t_sub, batch from practical')
        prac = db.cu.fetchall()
        res = res + prac
        try:
            if len(check) != 0:
                messagebox.showerror("Pynalyze", "Data table already exists !")
            else:
                for i in range(len(res)):
                    for j in range(c[0]):
                        # stmt = ("INSERT INTO feedback "
                        #         "(t_id, q_id, time) "
                        #         "values (%s, %s, %s);")
                        # data = (res[i], j+1, time_input)
                        stmt = ("INSERT INTO feedback "
                                "(t_id, q_id, time, t_sub, t_div) "
                                "value (%s, %s, %s, %s, %s);")
                        data = (res[i][0], j+1, time_input, res[i][1], res[i][2])
                        db.cu.execute(stmt, data)
                messagebox.showinfo("Pynalyze", "Table Created Successfully")
                db.db.commit()
        except pm.err:
            db.db.rollback()

    def show_report(self, report):
        print("starting")
        from dbase import DbConnect

        ttk.Label(report, text="Select Department").grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        dept_list = ttk.Combobox(report)
        time_box = ttk.Combobox(report)
        time_box.grid(row=1, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        dept_list.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)

        db = DbConnect(self.ip)
        db.cu.execute('SELECT dept FROM `department`')
        row = db.cu.fetchall()
        dept_list['values'] = row
        # dept = dept_list.get()
        # row = db.cu.fetchall()

        db.cu.execute('Select distinct(time) from feedback')
        row = db.cu.fetchall()
        time_box['values'] = row
        ttk.Button(report, text="Generate", command=lambda: self.make_report(dept_list.get(), time_box.get())). \
            grid(row=2, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        # lambda: self.make_report(dept_list.get()))

    def make_report(self, dept, time_in):
        print("initializing")
        time_in = time_in[1:-1]
        # import datetime
        from dbase import DbConnect
        db = DbConnect(self.ip)
        dept = str(dept)
        db.cu.execute("SELECT t_id, t_sub, t_div from teacher where dept=%s", dept)
        t_res = db.cu.fetchall()
        db.cu.execute('Select t_id, t_sub, batch from practical where dept=%s', dept)
        t_res = t_res+db.cu.fetchall()
        # db.cu.execute("SELECT t_id, t_sub, batch from practical where dept=%s", dept)
        # t_res.append(db.cu.fetchall())
        # print
        # time_input = datetime.date.today().strftime("%B %Y")
        # db.cu.execute("select distinct(time) from feedback")
        # time_in = db.cu.fetchone()
        # time_in = time_in[0]

        for detail in t_res:
            tid = detail[0]
            t_sub = detail[1]
            t_div = detail[2]
            # print(tid)
            # ---------------------------COLLECTING VARIABLES------------------------------
            db.cu.execute("Select t_name from mt_teacher where t_id={}".format(tid))
            r1 = db.cu.fetchone()
            t_name = r1[0]

            try:
                db.cu.execute("Select dept from teacher where t_id=%s and t_sub=%s and t_div=%s", (tid, t_sub, t_div))
                print((tid, t_sub, t_div))
                r1 = db.cu.fetchone()
                t_dept = r1[0]
            except TypeError:
                db.cu.execute("Select dept from practical where t_id=%s and t_sub=%s and batch=%s", (tid, t_sub, t_div))
                r1 = db.cu.fetchone()
                t_dept = r1[0]

            db.cu.execute("select sem from subjects where subject_name=%s and dept=%s", (t_sub, dept))
            r1 = db.cu.fetchone()
            t_sem = r1[0]

            # print(t_sub)
            # print t_sub
            db.cu.execute("Select AVG(avg) from feedback where t_id=(%s) and time=(%s) and t_sub=%s and t_div=%s",
                          (tid, time_in, t_sub, t_div))
            r1 = db.cu.fetchone()
            final_rating = r1[0]
            # print((tid, time_in, t_sub, t_div))
            final_rating = round(final_rating, 3)
            # ---------------------------WRITING IN FILE---------------------------------------------
            filepath = t_dept + "_" + time_in + "/" + str(t_sem)
            print(filepath, tid)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = t_name + "_" + t_sub + "_" + t_div
            # print(filename)
            f = open("{}/{}.txt".format(filepath, filename), "w+")
            f.write("==>Teacher name \t: {}\n".format(t_name))
            f.write("==>Subject \t\t: {}\n==>Department \t\t: {}\n".format(t_sub, t_dept))
            f.write("==>Division \t\t: {}\n".format(t_div))
            f.write("\n\t\t-----------------SCORE-----------------\n")
            db.cu.execute("Select avg from feedback where t_id=(%s) and time=(%s) and t_sub=(%s) and t_div=%s",
                          (tid, time_in, t_sub, t_div))
            avg = db.cu.fetchall()
            db.cu.execute("Select q_tag from mt_question")
            num_rows = db.cu.rowcount
            q_text = db.cu.fetchall()
            final_pct = (final_rating / 5) * 100
            #print(q_text.__len__())
            print(q_text)
            for x in range(0, num_rows):
                pct = (avg[x][0] / 5) * 100
                # f.write("%s)" % (x+1)+"%s" % str(q_text[0])+" - %s/5" % str(avg[0])+"\n\n")
                #print(q_text[x][0])
                print(num_rows)
                f.write("{}) {} % \t\t||{}\n\n".format(x + 1, round(pct, 2), q_text[x][0]))
            f.write("\n\t\t--------------TOTAL SCORE--------------\n")
            f.write("\t\t\t-----------------------\n\t\t\t   {} %\n\t\t\t-----------------------\n\n".
                    format(round(final_pct, 3)))
            f.write("_________________\n")
            f.write("   SIGNATURE")

            # self.make_graph(tid)
            db.cu.execute("select review from teacher_review "
                          "where t_id=%s and time=%s and t_sub=%s and t_div=%s", (tid, time_in, t_sub, t_div))
            rev = db.cu.fetchall()
            f.write("\n\n\n\n\n\n\n\n\n\n\n\n\t--------Reviews--------\n\n")
            for i in rev:
                f.write("\n{} \n".format(i[0]))
                print(rev)
            # self.make_graph(tid, filepath)
            f.close()
        messagebox.showinfo("Pynalyze", "Report Generated")

    def add_teacher(self, add_teacher):
        from dbase import DbConnect
        print("adding")

        ttk.Label(add_teacher, text="Select Department").grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        ttk.Label(add_teacher, text='Select Sem').grid(row=1, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        ttk.Button(add_teacher, text="Next",
                   command=lambda: self.select_teacher(sem_list.get(), dept_list.get(), add_teacher)) \
            .grid(row=2, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        dept_list = ttk.Combobox(add_teacher)
        sem_list = ttk.Combobox(add_teacher)
        dept_list.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        sem_list.grid(row=1, column=1, padx=10, pady=10, ipadx=5, ipady=5)

        db = DbConnect(self.ip)
        db.cu.execute('Select dept from department')
        res = db.cu.fetchall()
        dept_list['values'] = res
        sem = [1, 2, 3, 4, 5, 6, 7, 8]
        sem_list['values'] = sem

    def select_teacher(self, sem, dept, add_top):
        from dbase import DbConnect
        if sem == '' or dept == '':
            messagebox.showerror(title='Missing Value', message='department/sem values cannot be empty')
            add_top.lift()
            return
        if int(sem) > 2 and dept == 'AS&H':
            messagebox.showerror(title='Invalid Value', message='Error in department/sem values')
            add_top.lift()
            return
        elif int(sem) < 3 and dept != 'AS&H':
            messagebox.showerror(title='Invalid Value', message='Error in department/sem values')
            add_top.lift()
            return
        teacher_select = Toplevel(self)
        teacher_select.lift()
        teacher_type = ttk.Notebook(teacher_select)

        selection_top = ttk.Frame(teacher_select)
        selection_sp = ttk.Frame(teacher_select)
        teacher_type.add(selection_top, text="Normal")
        teacher_type.add(selection_sp, text="Special")
        teacher_type.grid()

        ttk.Label(selection_top, text="Teacher").grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        teacher = ttk.Entry(selection_top)

        teacher.grid(row=1, column=0, ipadx=5, ipady=5)
        ttk.Label(selection_top, text='Subject').grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        subject = ttk.Combobox(selection_top)
        db = DbConnect(self.ip)
        stmt = "select subject_name from subjects where sem=%s and dept=%s"
        data = (sem, dept)
        db.cu.execute(stmt, data)
        res = db.cu.fetchall()
        subject['values'] = res

        subject.grid(row=1, column=1, ipadx=5, ipady=5)
        ttk.Label(selection_top, text='Div').grid(row=0, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        div = ttk.Entry(selection_top)

        div.grid(row=1, column=2, ipadx=5, ipady=5)

        ttk.Button(selection_top, text='Add',
                   command=lambda:
                   self.add_teacher_list(teacher.get(), subject.get(), div.get(), teacher_select, 0)) \
            .grid(row=1, column=4, padx=10, pady=10, ipadx=5, ipady=5)

        ttk.Label(selection_sp, text="Teacher").grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        s_teacher = ttk.Entry(selection_sp)
        s_teacher.grid(row=1, column=0, ipadx=5, ipady=5)
        ttk.Label(selection_sp, text='Subject').grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        s_subject = ttk.Combobox(selection_sp)
        s_subject['values'] = res
        s_subject.grid(row=1, column=1, ipadx=5, ipady=5)
        ttk.Label(selection_sp, text='Batch').grid(row=0, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        s_div = ttk.Entry(selection_sp)
        s_div.grid(row=1, column=2, ipadx=5, ipady=5)

        ttk.Button(selection_sp, text='Add',
                   command=lambda:
                   self.add_teacher_list(s_teacher.get(), s_subject.get(), s_div.get(), teacher_select, 1)) \
            .grid(row=1, column=4, padx=10, pady=10, ipadx=5, ipady=5)

        ttk.Button(teacher_select, text='Save', command=lambda: self.teacher_save(sem, dept)) \
            .grid(row=4, column=3, padx=10, pady=10, ipadx=5, ipady=5)

        # stmt = 'select '

    def add_teacher_list(self, teacher, subject, div, selection_top, flag):
        from dbase import DbConnect
        label_list = []
        button_list = []
        if teacher == '' or subject == '' or div == '':
            messagebox.showerror(title="Missing Values", message="Please enter values correctly")
            return
        db = DbConnect(self.ip)
        stmt = 'select t_name from mt_teacher where t_id=%s'
        num = db.cu.execute(stmt, teacher)
        if num == 0:
            messagebox.showerror(title="Invalid", message="Teacher does not exist")
            return
        res = db.cu.fetchone()
        teacher_name = res[0]

        if flag == 0:
            self.teacher_value.append([teacher, teacher_name, subject, div.upper()])
        if flag == 1:
            self.sp_teacher_value.append([teacher, teacher_name, subject, div.upper()])
        teacher_box = Canvas(selection_top)
        teacher_box.grid(row=3, column=0, sticky=(N, S, E, W))

        self.teacher_refresh(teacher_box, label_list, button_list)

        '''for t in teacher_values:
            text = 'Name : '+t[0]+'    ||    Sub: '+t[1]+'    ||    Div: '+t[2]
            ttk.Label(teacher_box, text=text).grid(row=row_num, column=0, padx=5, pady=5, sticky=W)
            ttk.Button(teacher_box, text='Delete',
                       command=lambda: delete_teacher(teacher_values, row_num, teacher_box))\
                .grid(row=row_num, column=1, padx=5, pady=5, sticky=E)
            row_num += 1'''

    def teacher_save(self, sem, dept):
        from dbase import DbConnect
        db = DbConnect(self.ip)
        stmt = 'insert into teacher(t_id,t_sub,t_div,sem,dept) values(%s,%s,%s,%s,%s)'
        s_stmt = 'insert into practical(t_id,t_sub,batch,t_div,sem,dept) values(%s,%s,%s,%s,%s,%s)'
        stmt2 = 'insert into student(s_id,s_div,s_dept,s_sem, batch) values(%s,%s,%s,%s,%s)'
        stu_id = dept + "_" + sem + "_"
        print(stu_id)

        try:
            batch_list = []
            for t in self.teacher_value:
                data = [t[0], t[2], t[3], sem, dept]
                db.cu.execute(stmt, data)
            for t in self.sp_teacher_value:
                div = t[3][:1]
                data = [t[0], t[2], t[3], div, sem, dept]
                db.cu.execute(s_stmt, data)
                if batch_list.count(t[3]) == 0:
                    batch_list.append(t[3])
            if batch_list:
                for t in batch_list:
                    s_id = stu_id + t
                    check = 0
                    try:
                        check = db.cu.execute('select s_id from student where s_id = "{}" '.format(s_id))
                        print(check)
                    except pm.InternalError:
                        print(check)
                    if check == 0:
                        div = t[:1]
                        data = [s_id, div, dept, sem, t]
                        db.cu.execute(stmt2, data)
                        print("batch student")
                db.db.commit()
                messagebox.showinfo(title='Success', message='Teachers added successfully')
            else:
                for t in self.teacher_value:
                    s_id = stu_id + t[3]
                    check = 0
                    try:
                        check = db.cu.execute('select s_id from student where s_id = "{}" '.format(s_id))
                        print(check)
                    except pm.InternalError:
                        print(check)
                    if check == 0:
                        data = [s_id, t[3], dept, sem, '']
                        db.cu.execute(stmt2, data)
                        print("student")
                db.db.commit()
                messagebox.showinfo(title='Success', message='Teachers added successfully')
        except pm.err:
            db.db.rollback()
            messagebox.showerror()

    def delete_teacher(self, num, teacher_box, label_list, button_list, flag):
        if flag == 0:
            del self.teacher_value[num]
        if flag == 1:
            del self.sp_teacher_value[num]
        for l in label_list:
            l.destroy()
        label_list = []
        for b in button_list:
            b.destroy()
        button_list = []
        self.teacher_refresh(teacher_box, label_list, button_list)

    def teacher_refresh(self, teacher_box, label_list, button_list):
        row_num = 0
        for t in self.teacher_value:
            text = 'Name : ' + t[1] + '\t||\tSub:  ' + t[2] + '  \t||\tDiv: ' + t[3]
            label_list.append(ttk.Label(teacher_box, text=text))
            label_list[row_num].grid(row=row_num, column=0, padx=5, pady=5, sticky=W)
            button_list.append(ttk.Button(teacher_box, text='Delete',
                                          command=lambda x=row_num:
                                          self.delete_teacher(x, teacher_box, label_list, button_list, 0)))
            button_list[row_num].grid(row=row_num, column=1, padx=5, pady=5, sticky=E)
            row_num += 1
        count = 0
        for t in self.sp_teacher_value:
            text = 'Name : ' + t[1] + '\t||\tSub:  ' + t[2] + '  \t||\tDiv: ' + t[3]
            label_list.append(ttk.Label(teacher_box, text=text))
            label_list[row_num].grid(row=row_num, column=0, padx=5, pady=5, sticky=W)
            button_list.append(ttk.Button(teacher_box, text='Delete',
                                          command=lambda x=count:
                                          self.delete_teacher(x, teacher_box, label_list, button_list, 1)))
            button_list[row_num].grid(row=row_num, column=1, padx=5, pady=5, sticky=E)
            row_num += 1
            count += 1


''' def make_graph(self, x, path):

        from dbase import DbConnect
        db = DbConnect(self.ip)
        r = []
        stmt = """select avg from feedback where t_id=%s and q_id=%s"""
        for i in range(12):
            db.cu.execute(stmt, (x, i + 1))
            r.append(db.cu.fetchone()[0])
        db.cu.execute("Select t_name from mt_teacher where t_id=(%s)", x)
        name = db.cu.fetchone()[0]

        plt.rcdefaults()

        # from matplotlib.ticker import FormatStrFormatter
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.tick_params(axis='both', which='minor', labelsize=7)

        objects = ('EXPLANATION', 'OPPORTUNITY', 'STIMULATION', 'SYLLABUS COMP.', 'TIME USAGE', 'PAPER CORRECTION',
                   'COMM.', 'CLASS CONTROL', 'ATTITUDE', 'VICTIMIZATION', 'FAVOURITISM', 'PUNCTUAL')
        y_pos = np.arange(len(objects))

        performance = []
        for i in range(12):
            performance.append(r[i])
        print(performance)
        bar = plt.bar(y_pos, performance, width=0.75, color='y', align='center', alpha=1.0)

        bar[0].set_color('orange')
        bar[1].set_color('blue')
        bar[2].set_color('green')
        bar[3].set_color('purple')
        bar[4].set_color('red')
        bar[5].set_color('brown')
        bar[6].set_color('pink')
        bar[7].set_color('grey')
        bar[8].set_color('olive')
        bar[9].set_color('black')
        bar[10].set_color('yellow')
        bar[11].set_color('cyan')

        plt.xticks(y_pos, objects)
        plt.ylabel('Ratings')
        plt.title(name)
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        # plt.show()
        plt.savefig(path + '/' + name + '.pdf', bbox_inches='tight')
        plt.savefig(path + '/' + name + '.png', bbox_inches='tight')
        plt.close()
'''
