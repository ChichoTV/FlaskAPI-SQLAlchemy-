from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
engine = create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
Measure=Base.classes.measurement
Station=Base.classes.station
latest=dt.date(2017,8,23)
year_ago=latest-dt.timedelta(days=365)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br>'
        f'/api/v1.0/start<br>'
        f'/api/v1.0/start/end<br>'
        f'AVAILABLE DATE RANGES: (2010-01-01)-(2017-08-23)'
        )

@app.route("/api/v1.0/precipitation")
def prcp():
    session=Session(engine)
    lists=session.query(Measure.prcp,Measure.date).all()
    prcp=[p[0] for p in lists]
    dts=[d[1] for d in lists]
    mydict={}
    for num in range(len(dts)):
        mydict[dts[num]]=prcp[num]
    session.close()
    return jsonify(mydict)


@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    stations=session.query(Station.station).all()
    stations=[st[0] for st in stations]
    mydict1={}
    for num in range(len(stations)):
        mydict1[num]=stations[num]
    session.close()
    return jsonify(mydict1)

@app.route('/api/v1.0/tobs')
def tobs():
    session=Session(engine)
    temps=session.query(Measure.date,Measure.tobs).filter(Measure.station=="USC00519281",Measure.date>=year_ago).all()
    dts=[temp[0] for temp in temps]
    tmp=[temp[1] for temp in temps]
    mydict={}
    for num in range(len(dts)):
        mydict[dts[num]]=tmp[num]
    return jsonify(mydict)
    
@app.route('/api/v1.0/<start>')
def start_date(start):
    session=Session(engine)
    ret=session.query(func.min(Measure.tobs),func.max(Measure.tobs),func.avg(Measure.tobs)).filter(Measure.date>=start).all()
    temp=[]
    mydict={}
    keys=['min','max','avg']
    for num in range(len(ret[0])):
        temp.append(ret[0][num])
    for num in range(len(temp)):
        mydict[keys[num]]=temp[num]
    session.close()
    return jsonify(mydict)





@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    session=Session(engine)
    ret=session.query(func.min(Measure.tobs),func.max(Measure.tobs),func.avg(Measure.tobs)).filter(Measure.date>=start,Measure.date<=end).all()
    temp=[]
    mydict={}
    keys=['min','max','avg']
    for num in range(len(ret[0])):
        temp.append(ret[0][num])
    for num in range(len(temp)):
        mydict[keys[num]]=temp[num]
    session.close()
    return jsonify(mydict)







if __name__ == "__main__":
    app.run(debug=True)