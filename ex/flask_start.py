from flask import Flask, render_template, request, jsonify, flash, redirect
import psycopg2
import psycopg2.extras


app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = "dtt_enter_work"
DB_USER = "boonstation"
DB_PASS = "pg1234"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)


@app.route("/")
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT person.name, person.lastname, timeline.time_in, timeline.time_out, timeline.dates FROM timeline LEFT JOIN person ON person.person_id = timeline.person_id")
    # cur.execute("SELECT person.name, person.lastname, timeline.time_in, timeline.time_out, timeline.dates FROM timeline LEFT JOIN person ON person.person_id = timeline.person_id WHERE dates = '2021-12-03' ORDER BY dates asc , time_in asc")
    fetchTimeline = cur.fetchall()
    return render_template('index.html', fetchTimeline=fetchTimeline)


@app.route("/range", methods=["POST", "GET"])
def range():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        From = request.form['From']
        to = request.form['to']
        print(From)
        print(to)
        query = "SELECT person.name, person.lastname, timeline.time_in, timeline.time_out, timeline.dates FROM timeline LEFT JOIN person ON person.person_id = timeline.person_id WHERE dates BETWEEN '{}' AND '{}'".format(
            From, to)
        cur.execute(query)
        fetchTimelineRange = cur.fetchall()
        print(fetchTimelineRange)
        print(type(fetchTimelineRange))
        return jsonify({'htmlresponse': render_template('response.html', fetchTimelineRange=fetchTimelineRange)})


@app.route("/export")
def export():

    return ()


if __name__ == "__main__":
    app.run(debug=True)
    print("hello")
