# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Set up the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database into new model
Base = automap_base()

# Reflect the tables from the database into the model
Base.prepare(engine, reflect=True)

# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Set up Flask
app = Flask(__name__)


@app.route("/")
def home():
    return (
        "SurfsUp Welcome Page<br/><br/>"
        "Available routes are:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-06-23').all()

    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.date >= '2016-06-23').filter(Measurement.station == 'USC00519281').all()

    tobs_data = [tobs[0] for tobs in results]

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    temp_stats = {
        'min_temperature': results[0][0],
        'max_temperature': results[0][1],
        'avg_temperature': results[0][2]
    }

    return jsonify(temp_stats)


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temp_stats = {
        'min_temperature': results[0][0],
        'max_temperature': results[0][1],
        'avg_temperature': results[0][2]
    }

    return jsonify(temp_stats)



if __name__=='__main__':
    app.run(debug=True, port=5001)

#################################################
# Flask Routes
#################################################
