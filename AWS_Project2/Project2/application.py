import os
import sys
import datetime
from flask import Flask, render_template, request
import pymysql
import pymysql.cursors

application = app = Flask(__name__)

username = 'yash'
password = 'yashdani'
database = 'adb'
port = 3306
server = 'cloud-adb.c6dyuwuzxull.us-east-2.rds.amazonaws.com'

connection = pymysql.connect(server, username, password, database)

@app.route('/')
def home():
    return render_template('countall.html')


@app.route('/list', methods=['POST','GET'])
def list():
    if request.method == "POST":
        sid = int(request.form['sid'])
        cid = int(request.form['cid'])
        section = int(request.form['section'])
        cur = connection.cursor()
        cur.execute("select Availability from fall2019 where Course ='"+str(cid)+"'and Section ='"+str(section)+"' for update")
        row = cur.fetchall()
        if row[0][0] == 0:
            cur.close()
            connection.close()
            return "course full"

        cur.execute("insert into enrolled values ('"+str(sid)+"','"+str(cid)+"','"+str(section)+"')")
        rows = cur.fetchall();

        cur.execute("update fall2019 set Availability = Availability - 1 where Availability > 0 and Course ='"+str(cid)+"' and Section ='"+str(section)+"'")
        rows1 = cur.fetchall()
        connection.commit()

        cur.execute("select * from enrolled")
        rows3 = cur.fetchall()
        #print(rows3)
        cur.close()
        connection.close()
        return render_template('cresult.html', rows = rows3)


@app.route('/list2', methods=['POST','GET'])
def list2():
    cur = connection.cursor()
    cur.execute("select * from fall2019")
    rows = cur.fetchall()
    cur.close()
    return render_template('result.html', rows = rows)


@app.route('/list3', methods=['POST','GET'])
def list3():
    if request.method == "POST":
        sid = int(request.form['sid'])
        cur = connection.cursor()
        cur.execute("select courseid, section from enrolled where stdid ='"+str(sid)+"'")
        rows = cur.fetchall()
        cur.close()
        return render_template('result1.html', rows = rows)

if __name__ == "__main__":
    application.debug = True
    application.run()
