# import libraries
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import os
import numpy as np
import datetime as dt
from datetime import date

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
#
# Create an engine for the hawaii.sqlite database
# 10-Ins_Flask_with_ORM/Solved/app.py
# 10-Advanced-Data-Storage-and-Retrieval/3/Activities/11-Stu_Chinook/Solved/Stu_Chinook.ipynb
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save a references to the to measurement and station tables
Measurement = Base.classes.measurement
Station = Base.classes.station
#
# Flask Setup
app = Flask(__name__)
#
# Flask Routes
@app.route("/")
def welcome():
        """Available API routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a database session object: session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and precipitation values
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []
    for date, prcp in date_prcp:
        list_dict = {}
        list_dict[date] = prcp
        prcp_date_list.append(list_dict)
    session.close()
    return jsonify(prcp_date_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create a database session object: session (link) from Python to the DB
    session = Session(engine)

    # Query for the dates and precipitation values
    hawaii_stations = session.query(Station.station, Station.name).all()

    # Convert to list of dictionaries to jsonify
    HI_stations = {}
    for station, name in hawaii_stations:
        stations[station] = name

    session.close()
    return jsonify(HI_stations)

    @app.route("api/v1.0/tobs")
def tobs():
    # Create a database session object: session (link) from Python to the DB
    session = Session(engine)

    # Get the last date contained in the dataset and date from one year ago
    latest_record = session.query(Measurement.date).\
                order_by(Measurement.date.desc()).first()

    yr_from_latest_record = (dt.datetime.strptime(latest_record[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query for the dates and temperature values
    dates_temps = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= yr_from_latest_record).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    dates_tobs_list = []
    for date, tobs in dates_temps:
        dates_dict = {}
        dates_dict[date] = tobs
        dates_tobs_list.append(dates_dict)

    session.close()
    return jsonify(dates_tobs_list)
    
if __name__ == '__main__':
app.run(debug=True)