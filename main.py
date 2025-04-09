from datetime import datetime
from flight_analysis.models import FlightDatabase
from flight_analysis.visualizer import FlightVisualizer


def main():
    flight_db = FlightDatabase("csv_files/flights_test.csv")

    print("\n=== Sort by Date (Descending) ===")
    flight_db.sort_by_date(reverse=True)
    flight_db.display(6)

    print("\n=== Sort by Date (Ascending) ===")
    flight_db.sort_by_date(reverse=False)
    flight_db.display(6)

    print("\n=== Sort by Duration (Longest First) ===")
    flight_db.sort_by_duration(reverse=True)
    flight_db.display(3)

    print("\n=== Sort by Airline ===")
    flight_db.sort_by_airline()
    flight_db.display(3)

    print("\n=== Filter by Airline: Ryanair ===")
    ryanair_flights = flight_db.filter_by_airline("Ryanair")
    for f in ryanair_flights[:3]:
        print(f)

    print("\n=== Filter by Class: Business ===")
    for f in flight_db.filter_by_class("Business")[:3]:
        print(f)

    print("\n=== Filter by Reason: Business ===")
    for f in flight_db.filter_by_reason("Business")[:3]:
        print(f)

    print("\n=== Filter by Route: VKO -> AYT ===")
    for f in flight_db.filter_by_route("VKO", "AYT"):
        print(f)

    print("\n=== Filter by Date Range (2024-01-01 to 2024-12-31) ===")
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    for f in flight_db.filter_by_date_range(start, end)[:3]:
        print(f)

    print("\n=== Average Flight Duration ===")
    print(f"{flight_db.average_duration():.2f} minutes")

    print("\n=== Flights by Airline ===")
    print(flight_db.flights_by_airline())

    print("\n=== Flights by Aircraft ===")
    print(flight_db.flights_by_aircraft())

    print("\n=== Busiest Routes ===")
    for route, count in flight_db.busiest_routes():
        print(f"{route}: {count} flights")

    print("\n=== Unique Airlines ===")
    print(flight_db.unique_airlines())

    print("\n=== Unique Airports ===")
    print(flight_db.unique_airports())

    print("\n=== Most Used Airport ===")
    airport, count = flight_db.most_used_airport()
    print(f"{airport} ({count} uses)")

    print("\n=== Flight Hours per Airline ===")
    for airline, hours in flight_db.flight_hours_per_airline().items():
        print(f"{airline}: {hours} hours")

    print("\n=== Flight Hours per Year ===")
    for year, hours in flight_db.flight_hours_per_year().items():
        print(f"{year}: {hours:.2f} hours")

    print("\n=== Flights per Year ===")
    for year, flights in flight_db.flights_per_year().items():
        print(f"{year}: {flights} Flights")

    print("\n=== Total Flight Hours ===")
    print(f"{flight_db.total_flight_hours()} hours")

    # Visualizing the data
    visualizer = FlightVisualizer(flight_db)
    # visualizer.plot_flights_per_year()
    # visualizer.plot_top_routes()
    # visualizer.plot_class_distribution()
    # visualizer.plot_route_sankey()


if __name__ == "__main__":
    main()
