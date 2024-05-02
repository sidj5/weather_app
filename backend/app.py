from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

# OpenWeatherMap API URL
API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = "b92ee1d9f0faa2f02a4d512e5d027fd3"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form["city"]
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Get temperature in Celsius
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Check if the response contains the expected data structure
    if "main" in data and "temp" in data["main"] and "weather" in data and len(data["weather"]) > 0 and "description" in data["weather"][0]:
        weather_info = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
        return render_template("index.html", weather=weather_info)
    else:
        error_message = "Failed to retrieve weather information for the specified city."
        return render_template("index.html", error=error_message)

if __name__ == "__main__":
    app.run(debug=True)