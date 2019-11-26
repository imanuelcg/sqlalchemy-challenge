# importing libraries
import numpy as numpy
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setting up database 
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Set up Flask 
app = Flask(__name__)

# Flask routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Welcome to my website!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"//api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def rain():
    #Creating session from python to the db
    session = Session(engine)

    precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()
    
    session.close()
    return dict(precipitation_scores)

@app.route('/api/v1.0/stations')
# Return a JSON list of stations from the dataset.
def stations():
    session = Session(engine)
    result = session.query(Station.station).all()
    
    session.close()
    return dict(result)

@app.route('/api/v1.0/tobs')
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
def tobs_temp():
    session = Session(engine)
    previous_tobs = session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').all()
    session.close()
    return dict(previous_tobs)

@app.route('/api/v1.0/<start>')
def start(start=None):
    session = Session(engine)

    tobs_only = session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all()
    
    session.close()

    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

@app.route('/api/v1.0/<start>/<end>')
def start(start=None,end=None):
    session = Session(engine)

    tobs_only_2 = session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all()
    
    session.close()

    tobs_df_2 = pd.DataFrame(tobs_only_2)

    tavg = tobs_df_2["tobs"].mean()
    tmax = tobs_df_2["tobs"].max()
    tmin = tobs_df_2["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)


if __name__ == '__main__':
    app.run(debug=True)