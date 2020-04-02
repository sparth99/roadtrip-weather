import requests
import json
import polyline
from datetime import datetime, timedelta
from uszipcode import ZipcodeSearchEngine
from Step import Step
from darksky.api import DarkSky, DarkSkyAsync
import sys


steps = []

def get_routes_json(start,end):
    API_KEY = 'X'
    r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin='+start+'&destination='+end+'&alternatives=false&key='+API_KEY)
    j = r.json()
    return j

def assign_steps(routes):
    for route in routes['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                distance = step['distance']['value']
                duration = step['duration']['value']
                latitude = step['end_location']['lat']
                longitude = step['end_location']['lng']
                s = Step(distance,duration,latitude,longitude)
                steps.append(s)

def assign_time(steps):
    current_time = datetime.now()
    new_time = current_time
    for step in steps:
        new_time = new_time + timedelta(0,step.duration)
        step.time = new_time

def assign_zipcode(steps):
    search = ZipcodeSearchEngine()
    for step in steps:
        zipcodes = search.by_coordinate(step.latitude,step.longitude,returns=1)
        if len(zipcodes) > 0:
            zipcode_dict = next(iter(zipcodes))
            step.zipcode = zipcode_dict['Zipcode']
            step.city = zipcode_dict['City']
            step.state = zipcode_dict['State']

def get_weather(steps):
    API_KEY = 'X'
    darksky = DarkSky(API_KEY)

    for step in steps:
        a = darksky.get_time_machine_forecast(
            step.latitude,
            step.longitude,
            time = step.time
        )
        step.weather = a.currently

if __name__ == "__main__":
    routes = get_routes_json(sys.argv[1],sys.argv[2])
    assign_steps(routes)
    assign_time(steps)
    assign_zipcode(steps)
    get_weather(steps)
    print("Start")
    for step in steps:
        print("")
        print("---------------")
        print(str(round(step.distance * .0006213711922373339,2)),end=" miles")
        print("")
        print("---------------")
        print("")
        print(step.city, end=", ")
        print(step.state)
        print(step.time)
        print(step.weather.summary)
        print(step.weather.apparent_temperature)
    print("End")