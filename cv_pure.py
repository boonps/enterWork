import cv2
import psycopg2
import time as times
from pyzbar.pyzbar import decode
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


def select_pg_person(qr_code):
    cur.execute("SELECT person_id, name, lastname, qrcode, status  from person where qrcode = '{}'".format(qr_code))
    return cur.fetchall()


def insert_pg(person_id, time_now, date_now):
    cur.execute(
        "INSERT INTO timeline (person_id,time_in,date) VALUES ('{}','{}','{}')".format(person_id, time_now, date_now))
    conn.commit()
    return cur.rowcount


def select_pg_timeline(person_id, date_now):
    cur.execute(
        "SELECT *  from timeline where person_id = '{}'and date = '{}'".format(person_id, date_now))
    return cur.fetchall()


def update_pg(time_now, person_id, date_now):
    cur.execute("UPDATE timeline set time_out = '{}' where person_id = '{}' and date = '{}'".format(time_now, person_id,
                                                                                                    date_now))
    conn.commit()
    return cur.rowcount


def current_date(date_now):
    return date_now.strftime("%y-%m-%d")


def current_time(time_now):
    return time_now.strftime("%H:%M:%S")


def today_now():
    return datetime.now()


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    for code in decode(frame):
        times.sleep(2)
        person_rows = select_pg_person(code.data.decode('utf-8'))
        timeline_rows = select_pg_timeline(person_rows[0][0], current_date(today_now()))

        if len(timeline_rows) == 0:
            insert_pg(person_rows[0][0], current_time(today_now()), current_date(today_now()))
            print("Goo! Work a day {} {}".format(person_rows[0][1], person_rows[0][2]))
        else:
            update_pg(current_time(today_now()), person_rows[0][0], current_date(today_now()))
            print("Byee! Go Home")

    cv2.imshow('frame_z', frame)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
