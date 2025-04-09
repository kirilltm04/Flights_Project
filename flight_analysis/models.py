import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from collections import Counter, defaultdict


@dataclass
class Flight:
    date: datetime
    flight_number: str
    from_airport_name: str
    from_iata: str
    from_icao: str
    to_airport_name: str
    to_iata: str
    to_icao: str
    dep_time: datetime
    arr_time: datetime
    duration_minutes: int
    airline_name: str
    airline_iata: str
    airline_icao: str
    aircraft_name: str
    aircraft_icao: str
    registration: Optional[str]
    seat_number: str
    seat_type: str
    flight_class: str
    flight_reason: str

    @classmethod
    def from_row(cls, row):
        # Mapping for seat type
        seat_type_map = {
            '1': 'Window',
            '2': 'Middle',
            '3': 'Aisle'
        }

        # Mapping for flight class
        flight_class_map = {
            '1': 'Economy',
            '2': 'Business'
        }

        # Mapping for flight reason
        flight_reason_map = {
            '1': 'Leisure',
            '2': 'Business'
        }

        # Parse departure airport
        from_airport_name, from_iata, from_icao = cls.parse_airport(row['From'])

        # Parse arrival airport
        to_airport_name, to_iata, to_icao = cls.parse_airport(row['To'])

        # Parse the airline
        airline_name, airline_iata, airline_icao = cls.parse_airline(row['Airline'])

        # Parse the aircraft
        aircraft_name, aircraft_icao = cls.parse_aircraft(row['Aircraft'])

        return cls(
            date=pd.to_datetime(row['Date']),
            flight_number=row['Flight number'],
            from_airport_name=from_airport_name,
            from_iata=from_iata,
            from_icao=from_icao,
            to_airport_name=to_airport_name,
            to_iata=to_iata,
            to_icao=to_icao,
            dep_time=pd.to_datetime(row['Dep time']),
            arr_time=pd.to_datetime(row['Arr time']),
            duration_minutes=cls.parse_duration_to_minutes(row['Duration']),
            airline_name=airline_name,
            airline_iata=airline_iata,
            airline_icao=airline_icao,
            aircraft_name=aircraft_name,
            aircraft_icao=aircraft_icao,
            registration=row.get('Registration') or None,
            seat_number=row['Seat number'],
            seat_type=seat_type_map.get(str(row['Seat type']).strip(), 'Unknown'),
            flight_class=flight_class_map.get(str(row['Flight class']).strip(), 'Unknown'),
            flight_reason=flight_reason_map.get(str(row['Flight reason']).strip(), 'Unknown')
        )

    def __str__(self):
        reg_str = f" | Reg: {self.registration}" if self.registration else ""
        return (f"{self.date.date()} | {self.flight_number} | {self.from_airport_name} , IATA: {self.from_iata}, "
                f"ICAO: {self.from_icao} -> {self.to_airport_name}, IATA: {self.to_iata}, ICAO: {self.to_icao} | "
                f"{self.dep_time.time()} - {self.arr_time.time()} | {self.duration_minutes} min | "
                f"{self.airline_name}, IATA: {self.airline_iata}, ICAO: {self.airline_icao} | "
                f"Aircraft: {self.aircraft_name}, ICAO: {self.aircraft_icao} | {self.flight_class} | "
                f"Seat: {self.seat_number} ({self.seat_type}) | "
                f"Reason: {self.flight_reason}{reg_str}")

    @staticmethod
    def parse_duration_to_minutes(duration_str: str) -> int:
        """Convert 'HH:MM:SS' to total minutes."""
        h, m, s = map(int, duration_str.split(':'))
        return h * 60 + m + s // 60

    @staticmethod
    def parse_airport(airport_str: str):
        """Parse the airports columns and get the name, ICAO and IATA codes"""
        try:
            # Get the last part in parentheses for codes
            last_open_paren = airport_str.rfind('(')
            last_close_paren = airport_str.rfind(')')
            code_part = airport_str[last_open_paren + 1:last_close_paren]

            # The rest is the name
            name_part = airport_str[:last_open_paren].strip()

            # Split codes (format: IATA/ICAO)
            iata, icao = code_part.split('/')
            return name_part, iata.strip(), icao.strip()
        except Exception as e:
            raise ValueError(f"Could not parse airport string: '{airport_str}'") from e

    @staticmethod
    def parse_airline(airline_str: str):
        """Parse the airline column and get the name, ICAO and IATA codes"""
        try:
            last_open = airline_str.rfind('(')
            last_close = airline_str.rfind(')')
            code_part = airline_str[last_open + 1:last_close]
            iata, icao = code_part.split('/')
            name_part = airline_str[:last_open].strip()
            return name_part, iata.strip(), icao.strip()
        except Exception as e:
            raise ValueError(f"Could not parse airline string: '{airline_str}'") from e

    @staticmethod
    def parse_aircraft(aircraft_str: str):
        """Parse the aircraft column and get the name and ICAO code"""
        try:
            # Get the last part in parentheses for codes
            last_open_paren = aircraft_str.rfind('(')
            last_close_paren = aircraft_str.rfind(')')
            code_part = aircraft_str[last_open_paren + 1:last_close_paren]

            # The rest is the name
            name_part = aircraft_str[:last_open_paren].strip()
            return name_part, code_part
        except Exception as e:
            raise ValueError(f"Could not parse airport string: '{aircraft_str}'") from e


class FlightDatabase:
    def __init__(self, filepath):
        self.flights = self.load_flights(filepath)

    @staticmethod
    def load_flights(filepath):
        """Load flight data from CSV and convert to a list of Flight objects."""
        df = pd.read_csv(filepath)
        flights = [Flight.from_row(row) for col, row in df.iterrows()]
        return flights

    def display(self, n=5):
        """Display the first n Flight objects."""
        for flight in self.flights[:n]:
            print(flight)

    def sort_by_date(self, reverse=False):
        """Sort flights by date."""
        self.flights.sort(key=lambda f: f.date, reverse=reverse)

    def sort_by_duration(self, reverse=False):
        """Sort flights by flight duration in minutes."""
        self.flights.sort(key=lambda f: f.duration_minutes, reverse=reverse)

    def sort_by_airline(self):
        """Sort flights alphabetically by airline name."""
        self.flights.sort(key=lambda f: f.airline_name)

    def filter_by_airline(self, airline_name):
        """Return all flights operated by the given airline."""
        return [f for f in self.flights if f.airline_name.lower() == airline_name.lower()]

    def filter_by_class(self, flight_class):
        """Return all flights with a specific class (e.g., 'Economy')."""
        return [f for f in self.flights if f.flight_class == flight_class]

    def filter_by_reason(self, reason):
        """Return all flights by reason (e.g., 'Business', 'Leisure')."""
        return [f for f in self.flights if f.flight_reason == reason]

    def filter_by_route(self, from_iata, to_iata):
        """Return all flights between two IATA airport codes."""
        return [f for f in self.flights if f.from_iata == from_iata and f.to_iata == to_iata]

    def filter_by_date_range(self, start_date, end_date):
        """Return all flights within a given date range."""
        return [f for f in self.flights if start_date <= f.date <= end_date]

    def average_duration(self):
        """Calculate and return the average flight duration in minutes."""
        return sum(f.duration_minutes for f in self.flights) / len(self.flights)

    def flights_by_airline(self):
        """Return a Counter of flights grouped by airline."""
        return Counter(f.airline_name for f in self.flights)

    def flights_by_aircraft(self):
        """Return a Counter of flights grouped by aircraft."""
        return Counter(f.aircraft_name for f in self.flights)

    def busiest_routes(self):
        """Return the top 5 most frequent routes as (route, count) tuples."""
        routes = Counter(f"{f.from_iata}->{f.to_iata}" for f in self.flights)
        return routes.most_common(10)

    def unique_airlines(self):
        """Return a sorted list of all unique airline names."""
        return sorted(set(f.airline_name for f in self.flights))

    def unique_airports(self):
        """Return a sorted list of all unique airport names used."""
        airports = set()
        for f in self.flights:
            airports.add(f.from_airport_name)
            airports.add(f.to_airport_name)
        return sorted(airports)

    def most_used_airport(self):
        """Return the airport (by name) that appears most often as origin or destination."""
        from collections import Counter
        airport_counts = Counter()
        for f in self.flights:
            airport_counts[f.from_airport_name] += 1
            airport_counts[f.to_airport_name] += 1
        return airport_counts.most_common(1)[0]

    def total_flight_hours(self):
        """
        Calculate the total time spent flying across all flights, in hours.
        Returns:
            float: Total flight time in hours.
        """
        total_minutes = sum(f.duration_minutes for f in self.flights)
        return round(total_minutes / 60, 2)

    def flight_hours_per_airline(self):
        """
        Calculate total flight hours grouped by airline.
        Returns:
            dict: Mapping of airline names to total flight hours.
        """
        airline_hours = defaultdict(int)
        for f in self.flights:
            airline_hours[f.airline_name] += f.duration_minutes
        return {airline: round(minutes / 60, 2) for airline, minutes in airline_hours.items()}

    def flight_hours_per_year(self):
        """
        Calculate total flight time per year in hours, sorted by ascending year.
        Returns:
            dict: A dictionary mapping years to total flight hours, sorted by year.
        """
        hours_per_year = defaultdict(float)
        for f in self.flights:
            hours_per_year[f.date.year] += f.duration_minutes / 60.0
        return {year: round(minutes, 2) for year, minutes in hours_per_year.items()}

    def flights_per_year(self):
        """
        Calculate total flights number per year, sorted by ascending year.
        Returns:
            dict: A dictionary mapping years to total flights, sorted by year.
        """
        flights_per_year = defaultdict(int)
        for f in self.flights:
            flights_per_year[f.date.year] += 1
        return dict(sorted(flights_per_year.items()))  # Sorted by year ascending
