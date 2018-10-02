import datetime
import os
from dbase import DbConnect
db = DbConnect("")
dept = 'MECH'
db.cu.execute("SELECT t_id, t_sub, batch from practical where dept=%s", dept)
t_res = db.cu.fetchall()
print(t_res)
time_input = datetime.date.today().strftime("%B %Y")
db.cu.execute("select distinct(time) from feedback")
time_in = db.cu.fetchone()
time_in = time_in[0]

for detail in t_res:
    tid = detail[0]
    print(tid)
    # ---------------------------COLLECTING VARIABLES------------------------------
    db.cu.execute("Select t_name from mt_teacher where t_id={}".format(tid))
    r1 = db.cu.fetchone()
    t_name = r1[0]

    db.cu.execute("Select dept from practical where t_id={}".format(tid))
    r1 = db.cu.fetchone()
    t_dept = r1[0]

    t_sub = detail[1]
    t_div = detail[2]
    # print(t_sub)
    # print t_sub
    print(tid,time_in,t_sub,t_div)
    db.cu.execute("Select AVG(avg) from feedback where t_id=(%s) and time=(%s) and t_sub=%s and t_div=%s",
                  (tid, time_in, t_sub, t_div))
    r1 = db.cu.fetchone()
    final_rating = r1[0]
    print(final_rating)
    final_rating = round(final_rating, 3)
    # ---------------------------WRITING IN FILE---------------------------------------------
    filepath = t_dept + "_" + time_in
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = t_name + "_" + t_sub + "_" + t_div
    f = open("{}/{}.txt".format(filepath, filename), "w+")
    f.write("==>Teacher name \t: {}\n".format(t_name))
    f.write("==>Subject \t\t: {}\n==>Department \t\t: {}\n".format(t_sub, t_dept))
    f.write("==>Division \t\t: {}\n".format(t_div))
    f.write("\n\t\t-----------------SCORE-----------------\n")
    db.cu.execute("Select avg from feedback where t_id=(%s) and time=(%s) and t_sub=(%s) and t_div=%s",
                  (tid, time_in, t_sub, t_div))
    avg = db.cu.fetchall()
    num_rows = db.cu.rowcount
    db.cu.execute("Select q_tag from mt_question")
    q_text = db.cu.fetchall()
    final_pct = (final_rating / 5) * 100
    for x in range(0, num_rows):
        pct = (avg[x][0] / 5) * 100
        # f.write("%s)" % (x+1)+"%s" % str(q_text[0])+" - %s/5" % str(avg[0])+"\n\n")
        f.write("{}) {} %\t||{}\n\n".format(x + 1, round(pct, 2), q_text[x][0]))
    f.write("\n\t\t--------------TOTAL SCORE--------------\n")
    f.write("\t\t\t-----------------------\n\t\t\t\t{} %\n\t\t\t-----------------------\n\n".
            format(round(final_pct, 3)))
    f.write("_________________\n")
    f.write("   SIGNATURE")

    # self.make_graph(tid)
    db.cu.execute("select review from teacher_review where t_id=%s and time= %s", (tid, time_in))
    rev = db.cu.fetchall()
    f.write("\n\n\n\n\n\n\n\n\n\n\n\n\t--------Reviews--------\n\n")
    for i in rev:
        f.write("\n{} \n".format(i[0]))
    # self.make_graph(tid, filepath)
    f.close()
    print("done")
