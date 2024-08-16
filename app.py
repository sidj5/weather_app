from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    return time.strftime(format, time.localtime(value))

# OpenWeatherMap API URL
API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "b92ee1d9f0faa2f02a4d512e5d027fd3"

# OpenWeatherMap One Call API URL for historical weather data
HISTORICAL_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    start_time = time.time()

    city = request.form["city"]
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Get temperature in Celsius
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Calculate server latency
    server_latency = time.time() - start_time  # Calculate the server processing time

    # Check if the response contains the expected data structure
    if "main" in data and "temp" in data["main"] and "weather" in data and len(data["weather"]) > 0:
        weather_info = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "server_latency": server_latency  # Include server latency in the response
        }

        # Fetch historical weather data for the Next 2 days
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        historical_data = []

        for i in range(1, 2):  # Next 2 days
            timestamp = int(time.time()) - i * 86400  # 86400 seconds in a day
            params_historical = {
                "lat": lat,
                "lon": lon,
                "dt": timestamp,
                "appid": API_KEY,
                "units": "metric"
            }
            historical_response = requests.get(HISTORICAL_WEATHER_API_URL, params=params_historical)
            historical_json = historical_response.json()

            # Add only the 'list' from the response to the historical data
            if "list" in historical_json:
                historical_data.extend(historical_json["list"])

        return render_template("index.html", weather=weather_info, historical_data=historical_data)
    else:
        error_message = "Failed to retrieve weather information for the specified city."
        return render_template("index.html", error=error_message, server_latency=server_latency)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)