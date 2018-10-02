import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from dbase import DbConnect
from pylab import *
plt.rcdefaults()


def tg1(host):
    db = DbConnect(host)
    db.cu.execute('select distinct t_id from feedback')
    res = db.cu.fetchall()
    print(res[0])
    r = []
    x = []
    for t in res:
        db.cu.execute('select sum(sum) from feedback where t_id='+str(t[0]))
        row = db.cu.fetchone()
        x.append(int(float(row[0])))
        r.append(row)
        print(x)
    db.cu.execute('select distinct t_id from feedback')
    res = db.cu.fetchall()
    objects = [int(i[0]) for i in res]
    print(objects)
    #  objects = ('TIME SENSE', 'SUBJ COMMND', 'TEACHNG METHDS', 'HELPING ATT.', 'INTERACTION', 'COMM SKILLS', 'OTHERS')

    na = []
    for i in objects:
        db.cu.execute('select t_name from mt_teacher where t_id='+str(i))
        res = db.cu.fetchone()
        na.append(res[0])
        print(na)

    plt.bar(objects, x, align='center', alpha=1.0)
    plt.xticks(objects, na)
    plt.ylabel('Ratings')
    plt.title('Teachers - March 2017')
    figtext(.03, .03, "The highest value is "+str(max(x)))

    plt.show()
