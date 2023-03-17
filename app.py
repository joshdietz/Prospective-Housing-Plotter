# create a quick flask app to serve an html page with a form for an address
# and a button to submit the form
# and the form should submit to a route that will return the travel time
# and distance to work for each person in the persons.json file

# Path: app.py
import distance_tracker
import requests
import json
import sys
import os
from flask import Flask, render_template, request, send_from_directory, send_file
import pandas as pd

PROPOSED_HOUSE_HISTORY = "proposed_house_history.csv"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    persons = None
    area_map = None
    address_list = []

    if request.method == 'POST':
        address = request.form['address']
        try:
            if os.path.exists(PROPOSED_HOUSE_HISTORY):
                house_history = pd.read_csv(PROPOSED_HOUSE_HISTORY)
            else:
                house_history = pd.DataFrame({'address': []})
            if address not in house_history['address'].values:
                house_history = pd.concat([house_history, pd.DataFrame({'address': [address]})])
                house_history.to_csv(PROPOSED_HOUSE_HISTORY, index=False)
        except Exception as e:
            print(f"Failed to add {address} to history file: {e}")

        with open('persons.json', 'r') as f:
            persons = json.load(f)

        persons = persons['persons']
        for person in persons:
            travel_time, distance = distance_tracker.get_travel_time(address, person['work_address'])
            person['travel_time'] = travel_time
            person['distance'] = distance
            person['work_coordinates'] = distance_tracker.get_coordinates(person['work_address'])
            person['maps_link'] = distance_tracker.create_maps_link(address, person['work_address'])

        area_map = distance_tracker.map_plot(address, persons)
    elif request.method == 'GET':
        try:
            house_history = pd.read_csv(PROPOSED_HOUSE_HISTORY)
            house_history = house_history.dropna()
            address_list = house_history['address'].values
            print(address_list)
            if len(address_list) == 0:
                address_list = []
        except Exception as e:
            print(f"Failed to read history file: {e}")
            address_list = []

    return render_template("index.html", persons=persons, area_map=area_map, address_list=address_list)

@app.route('/analytics')
def analytics():
    try:
        house_history = pd.read_csv(PROPOSED_HOUSE_HISTORY)
        house_history = house_history.dropna()
        address_list = house_history['address'].values
        with open('persons.json', 'r') as f:
            persons = json.load(f)

        house_options = pd.DataFrame()
        house_options['Address'] = address_list
        house_options['Average Travel Time'] = None

        for person in persons['persons']:
            house_options[f"{person['name']} Travel time"] = None
            house_options[f"{person['name']} Travel time - Numeric"] = None

        for i, address in enumerate(address_list):
            for person in persons['persons']:
                travel_time, _ = distance_tracker.get_travel_time(address, person['work_address'])
                house_options.loc[i, f"{person['name']} Travel time"] = travel_time
                house_options.loc[i, f"{person['name']} Travel time - Numeric"] = float(travel_time.split(" ")[0])

        # for each row, determine the average travel time
        for i, row in house_options.iterrows():
            house_options.loc[i, 'Average Travel Time'] = int(row[[f"{person['name']} Travel time - Numeric" for person in persons['persons']]].mean())
            print(row[[f"{person['name']} Travel time - Numeric" for person in persons['persons']]])

        house_options = house_options.drop([f"{person['name']} Travel time - Numeric" for person in persons['persons']], axis=1)
        house_options = house_options.sort_values(by='Average Travel Time', ascending=True)
        # create a formatted table
        # drop the distance column
        table = house_options.to_html(index=False, justify='center', classes='table table-striped table-hover table-bordered table-sm justify-content-center')

        return render_template("analytics.html", table=table)

    except Exception as e:
        print(f"Failed to read history file: {e}")
        address_list = []
        return "Failed to read history file: {e}"

@app.route('/static/style.css')
def send_static():
    # send the styles file
    return send_file('resources/style.css')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')