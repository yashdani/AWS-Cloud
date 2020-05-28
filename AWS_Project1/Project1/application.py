import os
import sys
import datetime
from flask import Flask, render_template, request
from collections import Counter, defaultdict
from sklearn.neighbors.nearest_centroid import NearestCentroid
import sqlite3 as sql
import numpy as np
import redis
from sklearn.cluster import KMeans
from scipy.spatial import distance
import random

PEOPLE_PHOTO =  os.path.join('static','people_photo')

application = app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_PHOTO

@app.route('/')
def home():
    return render_template('countall.html')


@app.route('/list', methods=['POST','GET'])
def list():
    if request.method == "POST":
        s = int(request.form['k1'])
        starttime=time.time()
        con = sql.connect("quiz.db")
        cur = con.cursor()
        arr = []
        result = []
        y = []
        cur.execute("select Age, Height from minnow ")
        rows = cur.fetchone();
        while rows != None:
            if rows[0] != None:
                if rows[1] != None:
                    arr.append(rows)
            rows = cur.fetchone();
        val = np.array(arr)

        kmean = KMeans(n_clusters= s ).fit(val)
        result.append(kmean.inertia_)
        print(Counter(kmean.labels_))
        x = Counter(kmean.labels_)

        #centroid
        kcenter = kmean.cluster_centers_

        lent = len(kcenter)
        print(kcenter)
        #distance
        dist_c = distance.cdist(kcenter,kcenter,'euclidean')
        len_dist_c = len(dist_c)

        #counting points in cluster
        v,u = np.unique(kmean.labels_, return_counts = True)
        print(u)

        #length of cluster
        l = len(kmean.cluster_centers_)
        print(l)
        endtime = time.time()
        tt = endtime - starttime
        print(tt)
        return render_template('cresult.html', arr = kmean.cluster_centers_,tt = tt, result = result,count = x, u = u, l = l, lent = lent, dist_c = dist_c)

@app.route('/list1', methods=['POST','GET'])
def list1():
    if request.method == "POST":
        #s = int(request.form['cul1'])
        starttime=time.time()
        con = sql.connect("quiz.db")
        #con.row_factory = sql.Row
        cur = con.cursor()
        arr = []
        result = []
        y = []
        cur.execute("select CabinNum, Fare Height from minnow ")
        rows = cur.fetchone();
        while rows != None:
            if rows[0] != None:
                if rows[1] != None:
                    arr.append(rows)
            rows = cur.fetchone();
        val = np.array(arr)

        kmean = KMeans(n_clusters= 10 ).fit(val)
        result.append(kmean.inertia_)
        print(Counter(kmean.labels_))
        x = Counter(kmean.labels_)

        #centroid
        kcenter = kmean.cluster_centers_
        lent = len(kcenter)
        print(kcenter)
        #distance
        dist_c = distance.cdist(kcenter,kcenter,'euclidean')
        len_dist_c = len(dist_c)

        #counting points in cluster
        v,u = np.unique(kmean.labels_, return_counts = True)
        print(u)

        #length of cluster
        l = len(kmean.cluster_centers_)
        print(l)

        endtime = time.time()
        tt = endtime - starttime
        print(tt)

        return render_template('cresult.html', arr = kmean.cluster_centers_,tt = tt, result = result,count = x, u = u, l = l, lent = lent, dist_c = dist_c)


@app.route('/list2', methods=['POST','GET'])
def list2():
    if request.method == "POST":
        s = int(request.form['cul2'])
        c1 = request.form['col1']
        c2 = request.form['col2']
       # k = int(request.form['cent'])

        starttime=time.time()
        con = sql.connect("quiz.db")
        #con.row_factory = sql.Row
        cur = con.cursor()
        arr = []
        result = []
        y = []
        cur.execute("select "+ c1 +", "+ c2 +" Height from minnow ")
        rows = cur.fetchone();
        while rows != None:
            if rows[0] != None:
                if rows[1] != None:
                    arr.append(rows)
            rows = cur.fetchone();
        val = np.array(arr)

        kmean = KMeans(n_clusters= s).fit(val)
        result.append(kmean.inertia_)
        print(Counter(kmean.labels_))
        x = Counter(kmean.labels_)



        #centroid
        kcenter = kmean.cluster_centers_
        lent = len(kcenter)
        print(kcenter)




        #distance
        dist_c = distance.cdist(kcenter,kcenter,'euclidean')
        len_dist_c = len(dist_c)

        #counting points in cluster
        v,u = np.unique(kmean.labels_, return_counts = True)
        print(u)

        #length of cluster
        l = len(kmean.cluster_centers_)
        print(l)

        #v = []
        ##   for row in rows:
          #      v.append({'kcenter':row[0],'l':float(row[1])})


        endtime = time.time()
        tt = endtime - starttime
        print(tt)

        return render_template('cresult.html', arr = kmean.cluster_centers_,tt = tt, result = result,count = x, u = u, l = l, lent = lent, dist_c = dist_c, rows = v)


@app.route('/bargraph', methods = ['GET','POST'])
def bargraph():
    #mag1 = float(request.form['mag1'])
    #mag2 = float(request.form['mag2'])
    #print(rows)
    #value = []
    if request.method == "POST":
        n = int(request.form['cul2'])
        f1 = (request.form['col1'])
        f2 = (request.form['col2'])

        con = sql.connect("quiz.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        result = []
        value = []
        cur.execute("select "+f1+","+f2+" from minnow")
        rows = cur.fetchone();
        print(rows)
        while rows != None:
            if rows[0] != None:
                if rows[1] != None:
                    result.append(rows)
            rows = cur.fetchone();
        kmeans = KMeans(n_clusters = n).fit(result)
        clust_center = np.around(kmeans.cluster_centers_, decimals =1)
        xyz,count = np.unique(kmeans.labels_, return_counts = True)

    def myconverter(o):
        if isinstance(o, np.float32):
            return float(o)

    #dumped = json.dumps(clust_center, default=myconverter)
    #dumped1 = json.dumps(count, default=myconverter)
    print(clust_center)
    print(count)
    if result != None:
        for (re,i) in zip(clust_center,count):
            value.append({'lat':re.tolist(),'mag':int(i)})
        #print("sql "+ answer)
    #rows=[]
    # close database connection
    print(value)
    print("connection2")

    return render_template("graph.html", rows = value)


@app.route('/list6', methods=['POST','GET'])
def list6():
    if request.method == "POST":
        s = datetime.time()

        o = random.Random(random.randint(1,1000))
        mag = o.randint(0,1)
        p = []
        if mag == 0:
            p = os.path.join(app.config['UPLOAD_FOLDER'],'a.jpg')
        else:
            p = os.path.join(app.config['UPLOAD_FOLDER'],'b.jpg')
        e = datetime.time()

        tt = endtime - starttime
        return render_template('query1.html',tt = tt, s = s, e = e, p = p)


if __name__ == "__main__":
    application.debug = True
    application.run()
