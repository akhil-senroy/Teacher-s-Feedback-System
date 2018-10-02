import pymysql
import numpy as np
import matplotlib.pyplot as plt
from dbase import DbConnect

db = pymysql.connect(host="localhost", user="pynalyze", passwd="", db="pz")
cursor = db.cursor()
X = 318
r = []
stmt = """select avg from feedback where t_id=%s and q_id=%s"""
for i in range(12):
    cursor.execute(stmt, (X, i+1))
    r.append(cursor.fetchone()[0])
cursor.execute("Select t_name from mt_teacher where t_id=(%s)",(X))
name = cursor.fetchone()[0]

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
# manager.window.showMaximized()
# plt.show()
plt.savefig(name+'.pdf', bbox_inches='tight')
plt.savefig(name+'.png', bbox_inches='tight')


#def graphical():
