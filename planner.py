"""flask app for stargazing planner"""

from flask import Flask, request, render_template, session, redirect
import http.client
import json
import requests
import datetime
import os

"""set environmental variable for auth string"""
api_key = os.environ.get("authorization_string")

app = Flask(__name__)


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

        """Return the extracted object information"""
        return {"Name": object_name, "Type": object_type, "Sub Type": object_subType, "Constellation": constellation, "Right Ascension": right_ascension, "Declinition": declinition}
    except TypeError:
        error_message = "Invalid input data. Please enter valid name"
    #return(f"Type: {object_type}")
    #return(f"Sub Type: {object_subType}")
    print(f"Constellation: {constellation}")
    print(f"Right Ascension: {right_ascension}")
    print(f"Declinition: {declinition}")
    #print(data.decode("utf-8"))

#def raise_exceptions(exception, message):
#    return exception(message)


#raise raise_exceptions(KeyError, "Not a valid star or deep sky object"

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
        #"formatted": 0  # Set to 0 for raw timestamps
	"date": datetime.date.today()
    }

    response = requests.get(base_url, params=params)
    astronomical_data = response.json()

    return astronomical_data
    print(astronomical_data)


@app.route("/api/riseAndSetTimes", methods=["GET", "POST"])
def indexTwo():
    """
    Args: Latitude, Longitude
    Returns: Ephemeral data: Rise and set times
    """
    if request.method == "POST":
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        print(latitude)
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
          
        print(f"Sunrise (GMT+0): {sunrise}")
        print(f"Sunset (GMT+0): {sunset}")
        print(f"Civil Twilight Begin (GMT+0): {civil_twilight_begin}")
        print(f"Civil Twilight End (GMT+0): {civil_twilight_end}")
        print(f"Nautical Twilight Begin (GMT+0): {nautical_twilight_begin}")
        print(f"Nautical Twilight End (GMT+0): {nautical_twilight_end}")
        print(f"Astronomical Twilight Begin (GMT+0): {astronomical_twilight_begin}")
        print(f"Astronomical Twilight End (GMT+0): {astronomical_twilight_end}")
    else:
        print("Failed to fetch data.")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
