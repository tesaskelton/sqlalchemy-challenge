import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

recent_date = '2017-08-23'
year_prior_date = '2016-08-23'

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - returns preciption from date 2016-08-23 to 2017-08-23 <br/>"
        f"/api/v1.0/stations - returns all stations<br/>"
        f"/api/v1.0/tobs - returns preciptation from date 2016-08-23 to 2017-08-23 for most active station<br/>"
        f"/api/v1.0/api/v1.0/start - returns min, max and avg temps from start date given(replace start with date)<br/>"
        f"/api/v1.0/api/v1.0/start/end - returns min, max and avg temps in date range given(replace start and end with dates)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the last 12 months of precipitation data"""
    f"'Last 12 months of precipitation data <br/>"


    # 
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
      filter(Measurement.date <= recent_date).\
      filter(Measurement.date >= year_prior_date).\
        order_by(Measurement.date).\
        group_by(Measurement.date).\
        all()

    session.close()

    # Jsonify results

    return jsonify(results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
     session = Session(engine)

#     """"""
     results = session.query(Station.station, Station.name).all()

     session.close()


     return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

#     """Return 12 months of precipitation data for most active station"""
#     # 
    most_active =session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()

    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
      filter(Measurement.date <= recent_date).\
      filter(Measurement.date >= year_prior_date).\
      filter(Measurement.station == most_active[0]).\
        order_by(Measurement.date).\
        group_by(Measurement.date).\
        all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<date>")
def startDate(date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return min, max, avg temperatures greater or equal to date given"""
# 
    start_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= date).all()


    return jsonify(start_results)


@app.route("/api/v1.0/<start>/<end>")
def dateRange(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return min, max, avg temperatures greater or equal within the date range given"""
# 
    range_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()


    return jsonify(range_results)




if __name__ == '__main__':
    app.run(debug=True)
