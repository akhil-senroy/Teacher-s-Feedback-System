def make_report(ip, tid):
    from dbase import DbConnect
    db = DbConnect(ip)
    # ---------------------------COLLECTING VARIABLES------------------------------
    # cursor.execute("INSERT INTO table VALUES (%s, %s, %s)", (var1, var2, var3))
    db.cu.execute("Select t_name from mt_teacher where t_id={}".format(tid))
    r1 = db.cu.fetchone()
    t_name = r1[0]
    # print(t_name)
    # f=open("%s.txt"%t_name,"w+")
    # print t_name
    db.cu.execute("Select dept from teacher where t_id={}".format(tid))
    r1 = db.cu.fetchone()
    t_dept = r1[0]
    # print(t_dept)
    # print t_dept
    db.cu.execute("Select t_sub from teacher where t_id={}".format(tid))
    r1 = db.cu.fetchone()
    t_sub = r1[0]
    # print(t_sub)
    # print t_sub
    db.cu.execute("Select rating from finalfeedback where t_id=(%s)", tid)
    r1 = db.cu.fetchone()
    final_rating = r1[0]
    # print(final_rating)
    # print final_rating
    # ---------------------------WRITING IN FILE---------------------------------------------
    filename = t_name + "_" + t_dept
    f = open("%s.txt" % filename, "w+")
    # f.write("            \t\t\t\t\t\t\t\t\t%s\n\n"%t_name)
    f.write("==>Teacher name : %s\n" % t_name)
    f.write("==>Subject : %s\n==>Department : %s\n\n" % (t_sub, t_dept))
    f.write("\t\t-----------------SCORE---------------------\n\n")
    db.cu.execute("Select avg from feedback where t_id=(%s)", tid)
    avg = db.cu.fetchall()
    num_rows = db.cu.rowcount
    db.cu.execute("Select q_text from mt_question")
    q_text = db.cu.fetchall()
    for x in range(0, num_rows):
        # f.write("%s)" % (x+1)+"%s" % str(q_text[0])+" - %s/5" % str(avg[0])+"\n\n")
        f.write("{}) {}/5 \t\t\t|| {}\n\n".format(x+1, round(avg[x][0], 2), q_text[x][0]))
    f.write("\n\n\t\t-------------OVER ALL SCORE-----------------\n\n")
    f.write("\t\t\t\t----------\n\t\t\t       %s percent" % final_rating+"\n\t\t\t\t----------\n\n\n\n\n\n\n")
    f.write("            \t\t\t\t\t\t\t\t\t_________________\n")
    f.write("            \t\t\t\t\t\t\t\t\t    SIGNATURE")
    f.close()

make_report("192.168.0.3", 318)
