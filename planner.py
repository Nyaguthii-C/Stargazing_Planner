"""flask app for stargazing planner"""

from flask import Flask, request, render_template, session, redirect,send_file, abort
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import http.client
import json
import requests
import datetime
import os
from flask_cors import CORS
import base64
from PyAstronomy import pyasl
import numpy as np

"""set environmental variable for auth string"""
api_key = os.environ.get("authorization_string")
starchart_key = os.environ.get("starchart_authstring")

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)  # Enable CORS for all routes

@app.route("/")
def index():
    """link html template displaying on user side"""
    return render_template("searchItem.html")


@app.route("/api/search")
def search():
    """
    Args: object name 
    Returns: celestial coordinates, name, sub type and type
    """
    search_term = request.args.get("term", "  ")
    endpoint = f"/api/v2/search?term={search_term}&ra=&dec=&match_type=exact"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }

    """get data from API"""
    conn = http.client.HTTPSConnection("api.astronomyapi.com")
    conn.request("GET", endpoint, headers=headers)
    response = conn.getresponse()
    response_data = response.read()
    parsed_data = json.loads(response_data)
    conn.close()

    """Extract specific attributes"""
    try:
        stellarObject_info = parsed_data["data"][0]
        object_name = stellarObject_info["name"]
        object_type = stellarObject_info["type"]["name"]
        object_subType = stellarObject_info["subType"]["name"]
        constellation = stellarObject_info["position"]["constellation"]["name"]
        right_ascension = stellarObject_info["position"]["equatorial"]["rightAscension"]["string"]
        declinition = stellarObject_info["position"]["equatorial"]["declination"]["string"]
    except TypeError:
        error_message = "Invalid input data. Please enter valid name"
    return {"Name": object_name, "Type": object_type, "Sub Type": object_subType, "Constellation": constellation, "Right Ascension": right_ascension, "Declinition": declinition}


def get_astronomical_data(latitude, longitude):
    """
    Args: user  latitude , longitude
    Return: Ephemeral data: sunrise, sunset,
           civil_twilight, nautical_twilight, astronomical_twilight rise and set times
    """
    base_url = "https://api.sunrise-sunset.org/json"
    params = {
        "lat": latitude,
        "lng": longitude,
	"date": datetime.date.today()
    }

    response = requests.get(base_url, params=params)
    astronomical_data = response.json()

    return astronomical_data


@app.route("/api/riseAndSetTimes", methods=["GET", "POST"])
def indexTwo():
    """
    Args: Latitude, Longitude
    Returns: Ephemeral data: Rise and set times
    """
    if request.method == "POST":
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        
        if latitude and longitude:  # Check if coordinates are provided
            astronomical_data = get_astronomical_data(latitude, longitude)

            if "results" in astronomical_data:
                sunrise = astronomical_data["results"]["sunrise"]
                sunset = astronomical_data["results"]["sunset"]
                solar_noon = astronomical_data["results"]["solar_noon"]
                civil_twilight_begin = astronomical_data["results"]["civil_twilight_begin"]
                civil_twilight_end = astronomical_data["results"]["civil_twilight_end"]
                nautical_twilight_begin = astronomical_data["results"]["nautical_twilight_begin"]
                nautical_twilight_end = astronomical_data["results"]["nautical_twilight_end"]
                astronomical_twilight_begin = astronomical_data["results"]["astronomical_twilight_begin"]
                astronomical_twilight_end = astronomical_data["results"]["astronomical_twilight_end"]

                return render_template("searchItem.html", sunrise=sunrise, sunset=sunset, solar_noon=solar_noon, civil_twilight_begin=civil_twilight_begin, civil_twilight_end=civil_twilight_end, nautical_twilight_begin=nautical_twilight_begin, nautical_twilight_end=nautical_twilight_end, astronomical_twilight_begin=astronomical_twilight_begin, astronomical_twilight_end=astronomical_twilight_end)
        return render_template("searchItem.html", no_coordinates=True)  

"""DEFINE A FUNCTION TO TAKE IN COORDS, CONSTELLTION NAME TO GIVE STAR CHARTS"""
@app.route("/api/get-star-chart", methods=["GET"])
def starChart():
    """
    get starcharts from astronomy api
    Args: lat, long, constellation, date
    Return: starcharts for the relevant contellation, latitude and longitude
    """
    conn = http.client.HTTPSConnection("api.astronomyapi.com")

    payload = "{\"style\":\"inverted\",\"observer\":{\"latitude\":33.775867,\"longitude\":-84.39733,\"date\":\"2023-09-06\"},\"view\":{\"type\":\"constellation\",\"parameters\":{\"constellation\":\"ori\"}}}"

    headers = {
        'Authorization': f"Basic {starchart_key}"
    }

    conn.request("POST", "/api/v2/studio/star-chart", payload, headers)

    res = conn.getresponse()
    chart_data = res.read()
    star_chart_image_data_base64 = base64.b64encode(chart_data).decode('utf-8')
    try:
        chart_image = Image.open(BytesIO(chart_data))
        # Display the image using the default image viewer
        chart_image.show()
    except Exception as e:
        print(f"Error: {str(e)}")

    # Parse the JSON response to get the image URL
    import json
    try:
        response_data = json.loads(chart_data)
        image_url = response_data.get("data", {}).get("imageUrl")
    except json.JSONDecodeError as e:
        return f"Error: Unable to parse JSON response. {str(e)}", 500
    

    if not image_url:
        return "Error: Image URL not found in the API response.", 500

    # Redirect to the image URL
    return redirect(image_url)


""" return alt azimuth"""
def parse_ra(ra_str):
    # Split the RA string into hours, minutes, and seconds
    parts = ra_str.split()
    hours = float(parts[0].replace('h', ''))
    minutes = float(parts[1].replace('m', ''))
    seconds = float(parts[2].replace('s', ''))
    
    # Convert to degrees
    degrees = (hours + minutes / 60 + seconds / 3600) * 15
    return degrees


@app.route("/api/get-alt-azimuth", methods=["GET", "POST"])
def altaz():
    if request.method == "POST":
        date_str = request.form["date"]
        ra_str = request.form["ra"]
        dec = float(request.form["dec"])
        user_alt = float(request.form["local-altitude"])

        # Capture the user's geographical location
        user_latitude_str = request.form["latitude"]
        user_longitude_str = request.form["longitude"]

        #handle latitude exceptions
        if user_latitude_str.strip() == "":
            # Handle the case where latitude is empty (e.g., provide a default value or show an error message)
            return("Enter location latitude")
        else:
            try:
                # Attempt to convert the latitude to a float
                user_latitude = float(user_latitude_str)
            except ValueError:
                # Handle the case where latitude is not a valid float (e.g., show an error message)
                return("Enter valid latitude value")

        #handle longitude exceptions 
        if user_longitude_str.strip() == "":
            # Handle the case where longitude is empty (e.g., provide a default value or show an error message)
            return("Enter location longitude")
        else:
            try:
                # Attempt to convert the longitude to a float
                user_longitude = float(user_longitude_str)
            except ValueError:
                # Handle the case where longitude is not a valid float (e.g., show an error message)
                return("Enter valid longitude value")


        jd = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        jd = pyasl.jdcnv(jd)
        ra_degrees = parse_ra(ra_str)

        # Use LST in the calculation
        alt, az, _ = pyasl.eq2hor(jd, ra_degrees, dec, lat=user_latitude, lon=user_longitude, alt=user_alt)
        #alt, az, _ = pyasl.eq2hor(jd, ra_degrees, dec, observatory="HS")

        if alt < 0:
            message = "Object not visible at your location at this time."
        else:
            message = ""


        return render_template("searchItem.html", alt=alt, az=az, message=message)

    return render_template("searchItem.html", alt=None, az=None, message=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
