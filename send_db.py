from random import random, randrange
import psycopg2
from datetime import datetime, time

value = 'pasuras'
conn = psycopg2.connect(
    host="localhost",
    database="dtt_enter_work",
    user="boonstation",
    password="pg1234")

cur = conn.cursor()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%y-%m-%d")
time_gen = time(8, randrange(25, 35), randrange(0, 60))
time_morning = time(8, 30, 00)
time1 = time_morning.strftime("%H:%M:%S")
time_pm = time(12, 00, 00)


# time1 = time_pm.strftime("%H:%M:%S")
# print(time1, time_pm)

# cur.execute("SELECT person_id, name, lastname, qrcode, status  from person where qrcode = '{}'".format(value))
# person_rows = cur.fetchall()
def check():
    cur.execute("SELECT time_out from timeline where person_id = '{}'".format(1))
    return cur.fetchall()


tim = check()


for i in tim:
    if i[0] is None:
        print("ttttt")
    else:
        print("llll")

# if t[0][0] is None:
#     print("kKKKK")
# else:
#     print("LLLL")

# if cur.rowcount == 0:
#     cur.execute("INSERT INTO timeline (person_id,time_in,time_out,date) VALUES ('{}','{}','{}','{}')".format
#                 (1, 1, 2, 3))
#     conn.commit()
conn.close()

# if len(timeline_rows) == 0:
#     cur.execute(
#         "INSERT INTO timeline (person_id,time_in,time_out,date) VALUES ('{}','{}','{}','{}')".format(person_rows[0][0],
#                                                                                                      1, 2, 3))
# else:
#     print("Sorry me leaw na")

# if current_time > time1:
#     print('okkk')
# else:
#     print('Noo')
# for row in rows:
#     print("person_id = ", row[0])
#     print("name = ", row[1])
#     print("lastname = ", row[2])
#     print("qrcode = ", row[3])
#     print("status = ", row[4], "\n")
#
# print("Operation done successfully")


# while True:
# if now.hour >5:

#     print(time_gen)
#     print("Sorry")
# else:
#     # break
