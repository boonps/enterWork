import cv2
import psycopg2
from pyzbar.pyzbar import decode
from random import randrange
import time as times
from datetime import datetime, time

conn = psycopg2.connect(
    host="localhost",
    database="dtt_enter_work",
    user="boonstation",
    password="pg1234")

cur = conn.cursor()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

time_set_morning = time(8, 40, 00)
time_morning = time_set_morning.strftime("%H:%M:%S")
time_set_leave = time(16, 00, 00)
time_leave_work = time_set_leave.strftime("%H:%M:%S")
time_set_home = time(16, 30, 00)
time_home = time_set_home.strftime("%H:%M:%S")
test_after_new = time(13, 0, 00)
time_new_after = test_after_new.strftime("%H:%M:%S")


def today_now():
    return datetime.now()


def current_time(time_now):
    return time_now.strftime("%H:%M:%S")


def current_date(date_now):
    return date_now.strftime("%y-%m-%d")


def rand_time_in():
    return time(8, randrange(25, 35), randrange(0, 60))


def rand_time_in_after():
    return time(12, randrange(40, 59), randrange(0, 60))


def rand_time_out():
    return time(randrange(4, 5), randrange(30, 60), randrange(0, 60))


def select_pg_person(qr_code):
    cur.execute("SELECT person_id, name, lastname, qrcode, status  from person where qrcode = '{}'".format(qr_code))
    return cur.fetchall()


def select_pg_timeline(person_id, date_now):
    cur.execute(
        "SELECT *  from timeline where person_id = '{}'and date = '{}'".format(person_id, date_now))
    return cur.fetchall()


def insert_pg(person_id, time_now, date_now):
    cur.execute(
        "INSERT INTO timeline (person_id,time_in,date) VALUES ('{}','{}','{}')".format(person_id, time_now, date_now))
    conn.commit()
    return cur.rowcount


def update_pg(time_now, person_id, date_now):
    cur.execute("UPDATE timeline set time_out = '{}' where person_id = '{}' and date = '{}'".format(time_now,
                                                                                                    person_id,
                                                                                                date_now))
    conn.commit()
    return cur.rowcount


def forget_insert_pg(person_id, time_in, time_out, date):
    cur.execute("INSERT INTO timeline (person_id,time_in,time_out,date) VALUES ('{}','{}','{}','{}')".format
                (person_id, time_in, time_out, date))
    conn.commit()
    return cur.rowcount


def check_forget_pg(person_id):
    cur.execute(
        "SELECT time_out  from timeline where person_id = '{}'".format(person_id))
    return cur.fetchall()


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    for code in decode(frame):
        times.sleep(2)
        if current_time(today_now()):  # อย่าลืมเปลี่ยนเวลา
            person_rows = select_pg_person(code.data.decode('utf-8'))
            timeline_rows = select_pg_timeline(person_rows[0][0], current_date(today_now()))
            if len(timeline_rows) == 0:
                if current_time(today_now()) < time_morning:
                    if insert_pg(person_rows[0][0], current_time(today_now()), current_date(today_now())):
                        print("Goo! Work a day {} {}".format(person_rows[0][1], person_rows[0][2]))
                    else:
                        print("Try Again please")
                if time_morning < current_time(today_now()) < time_leave_work:
                    if insert_pg(person_rows[0][0], rand_time_in_after(), current_date(today_now())):
                        print("Goo! Work a day {} {}NEW".format(person_rows[0][1], person_rows[0][2]))
                    else:
                        print("Try Again please NEW")
            else:
                print("You have successfully scanned")

            if current_time(today_now()) >= time_leave_work:
                person_rows = select_pg_person(code.data.decode('utf-8'))
                timeline_rows = select_pg_timeline(person_rows[0][0], current_date(today_now()))
                timeline_rows_timeout = check_forget_pg(person_rows[0][0])
                if len(timeline_rows) != 0:
                    for i in timeline_rows_timeout:
                        if i[0] is None:
                            if update_pg(current_time(today_now()), person_rows[0][0], current_date(today_now())):
                                print("Byee! Go Home")
                            else:
                                print("Already")
                                pass
                else:
                    print("Try Again please")
            if current_time(today_now()) >= time_leave_work:
                person_rows = select_pg_person(code.data.decode('utf-8'))
                timeline_rows = select_pg_timeline(person_rows[0][0], current_date(today_now()))
                if len(timeline_rows) == 0:
                    forget_insert_pg(person_rows[0][0], rand_time_in(), current_time(today_now()),
                                     current_date(today_now()))
                    print("Byee! Go Home New")
            else:
                update_pg(current_time(today_now()), person_rows[0][0], current_date(today_now()))  # add new
                print("bye Afternoon")
                # print("Try Again please NEW2")

    cv2.imshow('frame_z', frame)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
