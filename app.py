#!/usr/bin/python

from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Resource, Api
from geocodio import GeocodioClient
from pyzomato import Pyzomato
import requests.exceptions


app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

#API KEYS
client = GeocodioClient('f46ef5bbdcfbbebd4dcc75c5b6cce9767ee744b')
zomato = Pyzomato('ac9ae8751e5e53622383740fd5a20d9c')


class Home(Resource):
    def get(self):
        r = requests.get('https://api.geocod.io/v1.3/geocode')
        r2 = requests.get('https://developers.zomato.com/api/v2.1/geocode')

        if(r.status_code == 500): 
            return {'message': "Geocodio is Down. Error code: 500"}
        elif(r2.status_code == 500):
            return {'message': "Zomato is Down. Error code: 500"}
        else: 
            {"about: this is home"}

    def post(self):
        r = requests.get('https://api.geocod.io/v1.3/geocode')
        r2 = requests.get('https://developers.zomato.com/api/v2.1/geocode')

        if(r.status_code == 500): 
            return {'message': "Geocodio is Down. Error code: " + r.status_code}
        elif(r2.status_code == 500):
            return {'message': "Zomato is Down. Error code: " + r.status_code}
        else: 
            address = request.get_json()
            addr_str = address.get('address')
            return redirect(url_for('restaurants', address=addr_str))

class Restaurants(Resource):
    def get(self, address):
        location = client.geocode(address) # coordinates to get latitude and longitude
    
        latitude = location['results'][0]['location']['lat']
        longitude = location['results'][0]['location']['lng']

        locationData = zomato.getByGeocode(latitude, longitude)
        zomatoData = locationData['nearby_restaurants']

        restaurantList = list()

        for restaurantAttribute in zomatoData:
            restaurant = {'name': restaurantAttribute['restaurant']['name'],
                'address': restaurantAttribute['restaurant']['location']['address'],
                'cuisines': restaurantAttribute['restaurant']['cuisines'],
                'rating': restaurantAttribute['restaurant']['user_rating']['aggregate_rating']
                }
            restaurantList.append(restaurant)
        return jsonify({'restaurants': restaurantList})


api.add_resource(Home, '/')
api.add_resource(Restaurants, '/restaurants/<string:address>')


if __name__ == '__main__':
    app.run(debug=True)