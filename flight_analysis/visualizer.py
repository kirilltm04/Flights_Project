import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import plotly.graph_objects as go
sns.set(style="whitegrid")


class FlightVisualizer:
    """
    A class to create various visualizations from a FlightDatabase object.
    """

    def __init__(self, flight_db):
        """
        Initialize the visualizer with a FlightDatabase instance.

        Args:
            flight_db (FlightDatabase): Instance of FlightDatabase containing flights.
        """
        self.flight_db = flight_db

    def plot_flights_per_year(self):
        """
        Plot the number of flights taken per year as a bar chart.
        """
        data = defaultdict(int)
        for flight in self.flight_db.flights:
            data[flight.date.year] += 1

        years = sorted(data.keys())
        counts = [data[year] for year in years]

        plt.figure(figsize=(8, 5))
        sns.barplot(x=years, y=counts, hue=years, palette="Blues_d", legend=False)
        plt.title("Flights Per Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Flights")
        plt.tight_layout()
        plt.show()

    def plot_top_routes(self, top_n=5):
        """
        Plot the top N busiest routes as a bar chart.

        Args:
            top_n (int): Number of top routes to display.
        """
        routes = Counter(f"{f.from_iata} → {f.to_iata}" for f in self.flight_db.flights)
        top_routes = routes.most_common(top_n)

        labels, counts = zip(*top_routes)

        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(labels), y=list(counts), hue=labels, palette="Oranges_r", legend=False)
        plt.title(f"Top {top_n} Busiest Routes")
        plt.xlabel("Route")
        plt.ylabel("Number of Flights")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_class_distribution(self):
        """
        Plot a pie chart showing the distribution of flight classes (e.g., Economy, Business).
        """
        class_counts = Counter(f.flight_class for f in self.flight_db.flights)

        labels = list(class_counts.keys())
        sizes = list(class_counts.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette("pastel"))
        plt.title("Flight Class Distribution")
        plt.tight_layout()
        plt.show()

    def plot_route_sankey(self, top_n=10):
        """
        Visualizes the top N flight routes using a Sankey diagram.

        Args:
            top_n (int): Number of top routes to display.
        """
        # Count top routes
        route_counts = Counter((f.from_iata, f.to_iata) for f in self.flight_db.flights)
        most_common = route_counts.most_common(top_n)

        airports = list(set([r[0] for r, _ in most_common] + [r[1] for r, _ in most_common]))
        airport_index = {airport: i for i, airport in enumerate(airports)}

        source_indices = [airport_index[route[0]] for route, _ in most_common]
        target_indices = [airport_index[route[1]] for route, _ in most_common]
        values = [count for _, count in most_common]

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=airports,
                color="blue"
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values
            ))])

        fig.update_layout(title_text="Flight Route Flow (Top Routes)", font=dict(size=10, color='darkblue'))
        fig.show()
