import requests
import json
import io
import os
import sys
import numpy as np
import urllib
import base64
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import dotenv

dotenv.load_dotenv()
matplotlib.use('agg')

GOOGLE_MAPS_API_KEY = os.getenv('API_KEY')

def create_maps_link(to_address: str, from_address: str):
    # create a google maps link to the address
    # return the link
    url = 'https://www.google.com/maps/dir/?api=1&origin={}&destination={}'.format(from_address, to_address)
    return url

def get_travel_time(to_address: str, from_address: str, time: str = "2023-05-14T08:00:00.00Z"):
    # get the travel time to work from the address
    # return the travel time in seconds
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}'.format(from_address, to_address, GOOGLE_MAPS_API_KEY)
    r = requests.get(url)
    data = r.json()
    try:
        travel_time = data['rows'][0]['elements'][0]['duration']['text']
        travel_distance = data['rows'][0]['elements'][0]['distance']['text']
    except:
        print(data)
        travel_time = 'N/A'
        travel_distance = 'N/A'

    return travel_time, travel_distance

def get_coordinates(address: str):
    # get the coordinates of the address
    # return the coordinates in a tuple
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, GOOGLE_MAPS_API_KEY)
    r = requests.get(url)
    data = r.json()
    try:
        coordinates = data['results'][0]['geometry']['location']
    except:
        coordinates = None

    return coordinates

def main():
    address = input('Enter an address: ')
    with open('persons.json', 'r') as f:
        persons = json.load(f)

    persons = persons['persons']

    for person in persons:
        am_travel_time, am_distance = get_travel_time(address, person['work_address'])
        person['travel_time'] = am_travel_time
        person['distance'] = am_distance

    for person in persons:
        print('{} lives {} away and will take {} to get to work'.format(person['name'], person['distance'], person['travel_time']))

def map_plot(address: str, persons):
    BBox = ((-123.0215,-122.4687,45.3343, 45.5607))
    map_img = plt.imread('image.png')

    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    # {'lat': 45.5019793, 'lng': -122.8247274} coordinates['lng'] coordinates['lat']
    # coordinates of potential home
    coordinates = get_coordinates(address)
    if coordinates != None:
        lat_home = float(coordinates['lat'])
        lng_home = float(coordinates['lng'])
        ax.scatter(lng_home, lat_home, zorder=1, alpha=0.5, s=20, c='r', label=f'Home')
        print(f'Home coordinates: {coordinates}')

    for person in persons:
        coordinates = get_coordinates(person['work_address'])
        lat_work = float(coordinates['lat'])
        lng_work = float(coordinates['lng'])
        ax.scatter(lng_work, lat_work, zorder=2, alpha=0.9, s=20, label=f'{person["name"]}')
        print(f'{person["name"]} coordinates: {coordinates}')
        if coordinates != None:
            plt.plot([lng_work, lng_home], [lat_work, lat_home], 'bo', c='k', alpha=0.3, zorder=1, linestyle="--")
            lng_avg = (lng_work + lng_home)/2
            lat_avg = (lat_work + lat_home)/2
            plt.text(lng_avg, lat_avg, person['travel_time'], alpha=0.6, zorder=3, c='k', rotation=10, weight='semibold', size='small', horizontalalignment='center')

    ax.set_title(f'Commute to work from "{address}"')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.legend(
        loc='upper center',
        ncols=2,
        fancybox=True,
        shadow=True,
        bbox_to_anchor=(0.5, -0.05)
    )
    # remove the axis and ticks
    ax.axis('off')
    ax.imshow(map_img, zorder=0, extent = BBox, aspect= 'equal')

    # save the figure base64 encoded bytes to string
    figfile = io.BytesIO()
    plt.savefig(figfile,format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue())
    uri = 'data:image/png;base64,' + urllib.parse.quote(figdata_png)
    plt.close()
    return uri

if __name__ == '__main__':
    main()