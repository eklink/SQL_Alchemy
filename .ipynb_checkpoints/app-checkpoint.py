{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#dependcies \n",
    "import datetime as dt\n",
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func, desc"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Database setup, create engine\n",
    "engine = create_engine('sqlite:///Resources/hawaii.sqlite', connect_args={'check_same_thread': False})\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "#database set-up\n",
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)\n",
    "\n",
    "#save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "\n",
    "#create session\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Flask set-up\n",
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with stat\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "c:\\users\\eklin\\appdata\\local\\programs\\python\\python37-32\\lib\\site-packages\\IPython\\core\\interactiveshell.py:3334: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "#Flask routes\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    return (f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/start_date/<start_date><br/>\"\n",
    "        f\"/api/v1.0/start_date/end_date/<start_date>/<end_date>\"\n",
    "           )\n",
    "\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "    \"\"\"Return a dictionary of all percipitation scores for the previous year\"\"\"\n",
    "    # Query all percipitation scores for the year\n",
    "    prcp_data_results = session.query(Measurement.date, Measurement.prcp).\\\n",
    "    filter(Measurement.date < '2017-08-24').filter(Measurement.date > '2016-08-23').\\\n",
    "    group_by(Measurement.date).order_by(desc(Measurement.date)).all()\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all percipitation scores\n",
    "    all_prcp_data = []\n",
    "    for prcp_score in prcp_data_results:\n",
    "        prcp_dict = {}\n",
    "\n",
    "        # Use `date` as a key and `prcp` as a value\n",
    "        prcp_dict[prcp_score.date] = prcp_score.prcp\n",
    "        \n",
    "        all_prcp_data.append(prcp_dict)\n",
    "\n",
    "    # Return a JSON representation of the dictionary\n",
    "    return jsonify(all_prcp_data)\n",
    "    \n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    \"\"\"Return a list of stations from the dataset\"\"\"\n",
    "    # Query all stations\n",
    "    station_results = session.query(Station.name).all()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    all_stations = list(np.ravel(station_results))\n",
    "\n",
    "    # Return a JSON representation of the list\n",
    "    return jsonify(all_stations)\n",
    "\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    \"\"\"Return a dictionary of all temperature observataions for the previous year\"\"\"\n",
    "    # Query all temperatures for the last year\n",
    "    tobs_data_results = session.query(Measurement.date, Measurement.tobs).\\\n",
    "    filter(Measurement.date < '2017-08-24').filter(Measurement.date > '2016-08-23').\\\n",
    "    group_by(Measurement.date).order_by(desc(Measurement.date)).all()\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all temperatures\n",
    "    all_tobs_data = []\n",
    "    for tobs_record in tobs_data_results:\n",
    "        tobs_dict = {}\n",
    "\n",
    "        # Use `date` as a key and `tobs` as a value\n",
    "        tobs_dict[tobs_record.date] = tobs_record.tobs\n",
    "        \n",
    "        all_tobs_data.append(tobs_dict)\n",
    "\n",
    "    # Return a JSON representation of the dictionary\n",
    "    return jsonify(all_tobs_data)\n",
    "\n",
    "@app.route(\"/api/v1.0/start_date/<start_date>\")\n",
    "def daily_normals(start_date):\n",
    "    \"\"\"Return TMIN, TAVG, and TMAX for all dates greater than and equal to the start date\"\"\"\n",
    "    # Will accept start date in the format '%m-%d' \n",
    "    # Create a query that will calculate and return the daily normals, \n",
    "    # i.e. the averages for tmin, tmax, and tavg for all historic data which is later or equal to a specific month and day        \n",
    "    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "    daily_normals_data = session.query(*sel).filter(func.strftime(\"%m-%d\", Measurement.date) >= start_date).all()\n",
    "    number_of_elements = print(str(len(daily_normals_data)))\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all daily normals\n",
    "    all_daily_normals = []\n",
    "    for tstats_record in daily_normals_data:\n",
    "        (min_tobs, max_tobs, avg_tobs) = tstats_record\n",
    "        daily_normals_dict = {}\n",
    "        daily_normals_dict[\"avg\"] = avg_tobs \n",
    "        daily_normals_dict[\"max\"] = max_tobs \n",
    "        daily_normals_dict[\"min\"] = min_tobs \n",
    "        all_daily_normals.append(daily_normals_dict)\n",
    "\n",
    "    # Return a JSON representation of the dictionary\n",
    "    return jsonify(all_daily_normals)\n",
    "\n",
    "# print(daily_normals('07-15'))\n",
    "\n",
    "@app.route(\"/api/v1.0/start_date/end_date/<start_date>/<end_date>\")\n",
    "def calc_temps(start_date, end_date):\n",
    "    \"\"\"Return the list: TMIN, TAVG, and TMAX for the dates between the start and date inclusively\"\"\"    \n",
    "    # Will accept start date and end date in the format '%Y-%m-%d' \n",
    "    # and return the minimum, average, and maximum temperatures for that range of dates   \n",
    "    vacation_daily_normals = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    ###vacation_stats = list(np.ravel(vacation_daily_normals))\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all daily normals\n",
    "    all_vac_daily_normals = []\n",
    "    for vac_stats in vacation_daily_normals:\n",
    "        (min_tmp, max_tmp, avg_tmp) = vac_stats\n",
    "        daily_vac_dict = {}\n",
    "        daily_vac_dict[\"avg\"] = avg_tmp \n",
    "        daily_vac_dict[\"max\"] = max_tmp \n",
    "        daily_vac_dict[\"min\"] = min_tmp \n",
    "        all_vac_daily_normals.append(daily_vac_dict)\n",
    "\n",
    "    # Return a JSON representation of the list\n",
    "    return jsonify(all_vac_daily_normals)\n",
    "\n",
    "#print(calc_temps('2017-07-15', '2017-07-22'))\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
