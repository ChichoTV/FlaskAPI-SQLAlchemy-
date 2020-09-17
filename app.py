from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
Measure=Base.classes.measurement
Station=Base.classes.station


app = Flask(__name__)

@app.route("/")
def home():
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br>'
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


if __name__ == "__main__":
    app.run(debug=True)