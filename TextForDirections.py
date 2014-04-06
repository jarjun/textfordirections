from flask import Flask, request, redirect
import twilio.twiml
from googlemaps import GoogleMaps
import requests
import json

 
app = Flask(__name__)

def direcs(loc1, loc2):
    ret = ""
    gmaps = GoogleMaps()
    
    try:
        directions = gmaps.directions(loc1, loc2)
    except:
        return "At least one invalid address. Please try again."
    
    ret += "Will take about " + directions['Directions']['Duration']['html'] + "\n"
    
    for step in directions['Directions']['Routes'][0]['Steps']:
        if "Destination will be on the" in step['descriptionHtml']:
            idx = step['descriptionHtml'].index("Destination")
            s = step['descriptionHtml'][:idx] + "\n" + step['descriptionHtml'][idx:]
            ret += s
        else:
            ret += step['descriptionHtml'] + "\n"
            
    a = ""
    inBracks = False
    for i in range(len(ret)):
        if ret[i] == "<":
            inBracks = True
        elif ret[i] == ">":
            inBracks = False;
        else:
            if inBracks == False:
                a += ret[i]
    return a
def local(loc, place):
    
    key = "AIzaSyD_tSC1PpJOba5eyW6NUjNbNZuH5wgpiTI"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters"
    
    query_params = { 'key': key,
                     'sensor': "false",
                     'rankby': 'distance',
                     'keyword':place,
                     'location' : loc
                      
                    }
    response = requests.get(url, params = query_params)
    data = response.json()
    return data

def geocode(loc):
    url = "https://maps.googleapis.com/maps/api/geocode/json?parameters"
    
    query_params = { 'address' : loc,
                    'sensor': 'false'
                    }
    response = requests.get(url, params = query_params)
    data = response.json()
    return data

def localSearchDirections(position, placeType):
    ret = ""
    geoData = geocode(position)
    lat = geoData['results'][0]['geometry']['location']['lat']
    lng = geoData['results'][0]['geometry']['location']['lng']
    latLong = str(lat) + ", " + str(lng)
    
    bigDataThing = local(latLong, placeType)
    name = bigDataThing['results'][0]['name']
    address = bigDataThing['results'][0]['vicinity']
    ret += "Name: " + name + "\n"
    ret += "Address: " + address + "\n"
    ret += "Directions (Driving): \n" + direcs(position, address)
    if(len(ret) >= 1600):
        return "Nothing close. Please try again."
    else:
        return ret

@app.route("/", methods=['GET', 'POST'])
def get_directions():
    toGet = request.values.get('Body', None)
    if ";" not in toGet:
        message = "Please put a semicolon between the address and place type."
    else:
        blah = toGet.split(";")
        message = localSearchDirections(blah[0],blah[1])
    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)