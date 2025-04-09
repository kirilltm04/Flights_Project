from flask import Flask, render_template, request
from flight_analysis.models import FlightDatabase

app = Flask(__name__)
db = FlightDatabase("csv_files/flights_test.csv")

# Define available actions for buttons
ACTIONS = [
    "sort_by_date",
    "sort_by_duration",
    "sort_by_airline",
    "average_duration",
    "flights_by_airline",
    "flights_by_aircraft",
    "busiest_routes",
    "most_used_airport",
    "total_flight_hours",
    "flight_hours_per_airline",
    "flight_hours_per_year",
    "flights_per_year",
    "unique_airlines",
    "unique_airports"
]


@app.route("/", methods=["GET", "POST"])
def index():
    action = request.form.get("action")
    result = None
    title = None

    if action == "sort_by_date":
        db.sort_by_date(reverse=True)
        title = "Flights sorted by date"
        result = db.flights

    elif action == "sort_by_duration":
        db.sort_by_duration(reverse=True)
        title = "Flights sorted by duration"
        result = db.flights

    elif action == "sort_by_airline":
        db.sort_by_airline()
        title = "Flights sorted by airline"
        result = db.flights

    elif action == "average_duration":
        title = "Average Flight Duration"
        result = f"{db.average_duration():.2f} minutes"

    elif action == "flights_by_airline":
        title = "Flights by Airline"
        result = db.flights_by_airline().most_common()

    elif action == "flights_by_aircraft":
        title = "Flights by Aircraft"
        result = db.flights_by_aircraft().most_common()

    elif action == "busiest_routes":
        title = "Top 10 Busiest Routes"
        result = db.busiest_routes()

    elif action == "most_used_airport":
        title = "Most Used Airport"
        result = db.most_used_airport()

    elif action == "total_flight_hours":
        title = "Total Flight Hours"
        result = f"{db.total_flight_hours()} hours"

    elif action == "flight_hours_per_airline":
        title = "Flight Hours per Airline"
        result = db.flight_hours_per_airline().items()

    elif action == "flight_hours_per_year":
        title = "Flight Hours per Year"
        result = db.flight_hours_per_year().items()

    elif action == "flights_per_year":
        title = "Flights per Year"
        result = db.flights_per_year().items()

    elif action == "unique_airlines":
        title = "Unique Airlines"
        result = db.unique_airlines()

    elif action == "unique_airports":
        title = "Unique Airports"
        result = db.unique_airports()

    return render_template("index.html", title=title, result=result, actions=ACTIONS)


if __name__ == "__main__":
    app.run(debug=True)
