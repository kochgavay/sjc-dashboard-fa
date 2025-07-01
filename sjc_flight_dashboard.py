import streamlit as st
import math
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh
import os
import time
from AeroAPI import AeroAPI

# ==== CONFIG ====
HOME_LAT = 37.399746   # your home latitude
HOME_LON = -121.962585  # your home longitude
MAX_DISTANCE_KM = 3.2  # 2 miles

# Airline code lookup (callsign prefixes)
AIRLINE_CODES = {
    "UAL": "United Airlines",
    "SWA": "Southwest",
    "DAL": "Delta",
    "ASA": "Alaska",
    "AAL": "American Airlines",
    "JBU": "JetBlue",
    "FFT": "Frontier",
    "SKW": "SkyWest",
    "NKS": "Spirit",
    "HXA": "Hawaiian Airlines",
    "Y4": "Volaris",
    "ZG": "ZIPAIR"
}

# Aircraft type lookup (partial, expand as needed)
AIRCRAFT_TYPES = {
    "A319": "Airbus A319",
    "A320": "Airbus A320",
    "A20N": "Airbus A320neo",
    "A332": "Airbus A330-200",
    "A343": "Airbus A340-300",
    "B712": "Boeing 717-200",
    "B734": "Boeing 737-400",
    "B737": "Boeing 737-700",
    "B738": "Boeing 737-800",
    "B739": "Boeing 737-900",
    "B763": "Boeing 767-300",
    "B788": "Boeing 787-8",
    "B789": "Boeing 787-9",
    "CRJ2": "Bombardier CRJ-200",
    "CRJ7": "Bombardier CRJ-700",
    "CRJ9": "Bombardier CRJ-900",
    "E75L": "Embraer ERJ-175",
    "MD90": "McDonnell Douglas MD-90"
}

# ICAO to city name mapping for major airports
ICAO_TO_CITY = {
    "KSFO": "San Francisco",
    "KLAX": "Los Angeles",
    "KSJC": "San Jose",
    "KSEA": "Seattle/Tacoma",
    "KDEN": "Denver",
    "KORD": "Chicago (O'Hare)",
    "KDFW": "Dallas/Fort Worth",
    "KPHX": "Phoenix",
    "KJFK": "New York",
    "KATL": "Atlanta",
    "KPDX": "Portland",
    "KLAS": "Las Vegas",
    "KOAK": "Oakland",
    "KSAN": "San Diego",
    "KDAL": "Dallas (Love Field)",
    "KMDW": "Chicago (Midway)",
    "KDTW": "Detroit",
    "KGEG": "Spokane",
    "KSTL": "St. Louis",
    "KMSP": "Minneapolis/St. Paul",
    "KONT": "Ontario",
    "KSNA": "Orange County (Santa Ana)",
    "KPSP": "Palm Springs",
    "KLGB": "Long Beach",
    "KBOI": "Boise",
    "KBUR": "Burbank",
    "KEUG": "Eugene",
    "KHOU": "Houston (Hobby)",
    "KIAH": "Houston (Intercontinental)",
    "KBNA": "Nashville",
    "KAUS": "Austin",
    "KBWI": "Baltimore/Washington",
    "KRNO": "Reno/Tahoe",
    "KSLC": "Salt Lake City",
    "PHOG": "Kahului (Maui)",
    "PHKO": "Kona (Big Island)",
    "KLIH": "Lihue",
    "MMGL": "Guadalajara",
    "MMLO": "León (Guanajuato)",
    "MMMM": "Morelia",
    "MMPR": "Puerto Vallarta",
    "MMSD": "San José del Cabo (Los Cabos)",
    "MMZC": "Zacatecas",
    "RJAA": "Tokyo–Narita",
}

# ==== FLIGHTAWARE CONFIG ====
FLIGHTAWARE_API_KEY = 'gjHfOw8lEoR3eck5zN50DTGFeSnyxxPy'
aeroapi = AeroAPI(FLIGHTAWARE_API_KEY)

# ==== FUNCTIONS ====
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_flights_near_home():
    # Use AeroAPI to get flights near home location
    # The radius is in kilometers
    try:
        flights = aeroapi.flights.get_flights_nearby(HOME_LAT, HOME_LON, MAX_DISTANCE_KM)
        return flights
    except Exception as e:
        st.error(f"Error fetching flight data from FlightAware: {e}")
        return []

def extract_details(flight):
    # flight is a dict from AeroAPI
    destination_icao = flight.get('destination')
    destination = ICAO_TO_CITY.get(destination_icao, destination_icao or "Unknown")
    airline = flight.get('operator', "Private")
    aircraft_type_code = flight.get('aircraft_type', "Unknown")
    aircraft_type = AIRCRAFT_TYPES.get(aircraft_type_code, aircraft_type_code)
    return destination, airline, aircraft_type

# ==== UI ====
st.set_page_config(page_title="Flights Overhead from SJC", layout="centered")
st.title("🛫 Flights Overhead")
now_pst = datetime.now(ZoneInfo("America/Los_Angeles"))
st.caption(f"Live from SJC | {now_pst.strftime('%Y-%m-%d %I:%M:%S %p')} PST")

flights = get_flights_near_home()
visible = []

for flight in flights:
    destination, airline, aircraft_type = extract_details(flight)
    visible.append({
        "Destination": destination,
        "Airline": airline,
        "Aircraft Type": aircraft_type
    })

if visible:
    for flight in visible:
        st.markdown(f"""
        <div style="padding:15px; margin-bottom:15px; border-radius:10px; background-color:#343434;">
            <div style="font-size:2rem; font-weight:bold;">{flight['Destination']}</div>
            <div style="font-size:1rem;">{flight['Airline']}</div>
            <div style="font-size:1rem;">{flight['Aircraft Type']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="padding:20px; margin-top:20px; text-align:left; font-size:1.5rem; color:#555;">
        🌤️ Clear skies!
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
@media (max-width: 768px) {
    .stApp { padding: 10px; font-size: 16px; }
    h1 { font-size: 1.5rem !important; }
}
</style>
""", unsafe_allow_html=True)