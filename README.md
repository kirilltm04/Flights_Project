# ✈️ Flights Project

The **Flights Project** is a web-based flight history analysis tool that allows users to explore, sort, and gain insights into personal or collected flight data through a clean and interactive web interface built with **Flask**. It parses CSV flight logs, constructs flight objects, and provides powerful analytics such as total flight hours, busiest routes, airline statistics, and more.

---

## 📌 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Folder Structure](#-folder-structure)
- [Sample Data](#-sample-data)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
  - [Flask App (`app.py`)](#flask-app-apppy)
  - [Data Model (`models.py`)](#data-model-modelspy)
  - [Frontend (`index.html` + `style.css`)](#frontend-indexhtml--stylecss)
- [License](#-license)
- [Contributing](#-contributing)
- [Questions?](#-questions)

---

## 🚀 Features

- Load and parse flight logs from CSV
- Sort flights by date, duration, or airline
- View average duration and total flight hours
- Analyze flights per year, airline, and aircraft
- Identify most used airports and busiest routes
- Clean HTML user interface with categorized results
- Fast and lightweight—runs entirely on your machine

---

## 🛠️ Installation

### 1. Clone the repository

~~~bash
git clone https://github.com/yourusername/flights-project.git
cd flights-project
~~~

### 2. Create a virtual environment (optional but recommended)

~~~bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
~~~

### 3. Install dependencies

~~~bash
pip install flask
~~~

### 4. Run the app

~~~bash
python app.py
~~~

### 5. Open in your browser
Sample view:
<img width="1024" alt="image" src="https://github.com/user-attachments/assets/c9d504f6-f61f-44e2-b0bc-da8064f44e45" />

---

## 📁 Folder Structure

```
flights-project/
├── flight_analysis/
│   └── models.py         # Data model: Flight, FlightDatabase
├── static/
│   └── style.css         # Custom CSS styling
├── templates/
│   └── index.html        # Main web interface
├── flights.csv           # Your flight data
├── app.py                # Flask backend
└── README.md             # You're reading it!
```

---

## Samle Data

The `flights_test.csv` file has a view like:

```csv
Date,"Flight number",From,To,"Dep time","Arr time",Duration,Airline,Aircraft,Registration,"Seat number","Seat type","Flight class","Flight reason",Note,Dep_id,Arr_id,Airline_id,Aircraft_id
2019-10-26,TK181,Cancun / Cancun (CUN/MMUN),Istanbul / Istanbul Airport (IST/LTFM),10:10:00,06:15:00,12:05:00,Turkish Airlines (TK/THY),Boeing 777-300ER (B77W),,31K,1,1,1,,639,8949,769,2023
2018-07-29,FR4513,Krakow / John Paul II International (KRK/EPKK),Tenerife-South / Reina Sofia (TFS/GCTS),13:05:00,17:15:00,05:10:00,Ryanair (FR/RYR),Boeing 737-800 (B738),,14E,2,1,1,,1489,2897,668,231
2018-08-15,FR4514,Tenerife-South / Reina Sofia (TFS/GCTS),Krakow / John Paul II International (KRK/EPKK),06:15:00,12:30:00,05:15:00,Ryanair (FR/RYR),Boeing 737-800 (B738),,24A,1,1,1,,2897,1489,668,231
2017-12-27,TK1,Istanbul / Istanbul Airport (IST/LTFM),New York / John F Kennedy (JFK/KJFK),15:05:00,18:15:00,10:10:00,Turkish Airlines (TK/THY),Boeing 777-300ER (B77W),,40C,3,1,1,,8949,1328,769,2023
2017-12-29,B61261,New York / John F Kennedy (JFK/KJFK),Barbados I / Bridgetown-Grantley Adams (BGI/TBPB),08:00:00,12:35:00,04:35:00,JetBlue Airways (B6/JBU),Airbus A321-200 (A321),,9A,1,1,1,,1328,287,410,2076

```

---

## 🧑‍💻 Usage

Once the app is running in your browser:

- Click any of the buttons (e.g. Sort By Date, Total Flight Hours) to trigger analysis.
- Results will display below, either as text, lists, or flight cards.
- Data is refreshed automatically on each action.
- To update your data, simply replace `flights.csv` and restart the app.

---

## ⚙️ How It Works

### Flask App (`app.py`)

The Flask app handles routing and interactions between the frontend and backend. It listens for POST requests with a selected action and returns the results. Each button corresponds to a method inside `FlightDatabase`. For example:

~~~python
elif action == "average_duration":
    result = f"{db.average_duration():.2f} minutes"
~~~

The results are passed to the template and rendered accordingly.

### Data Model (`models.py`)

The `FlightDatabase` class handles:

- Parsing and storing flights from CSV
- Sorting (by date, duration, airline)
- Analyzing (total hours, per airline/year, busiest routes)
- Utility functions for duration conversion and airport lookup

Each flight is represented by a `Flight` object containing fields such as:

- `date`, `flight_number`
- `from_airport_name`, `to_airport_name`
- `airline_name`, `aircraft_name`
- `duration_minutes`, `flight_class`, etc.

### Frontend (`index.html` + `style.css`)

- **index.html:** Renders buttons and results dynamically using Jinja2.
- **style.css:** Styles flight cards, grids, and overall layout.

Each flight card is neatly structured:

```html
<div class="flight-card">
  <div class="flight-header">
    {{ item.date }} | {{ item.flight_number }} | {{ item.airline_name }}
  </div>
  <!-- Additional flight details -->
</div>
```


## 🪪 License  
This project is licensed under the GNU General Public License v3.0. You are free to use, share, modify, and distribute this software under the terms of the GNU GPL v3.

## 🧭 Contributing  
Pull requests and suggestions are welcome! If you'd like to add more features—like charts, export tools, or maps—feel free to fork the project or open an issue.

## 💬 Questions?  
Feel free to reach out or open an issue on GitHub if you need help setting things up or extending the functionality. Made with ❤️ for flight enthusiasts.
