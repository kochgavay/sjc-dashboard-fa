import streamlit as st
from time import sleep

# --- Mappings (from your JS) ---
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

# --- Sample Data (from your JS, trimmed for brevity) ---
SAMPLE_FLIGHTS = [
    {
        "ident": "ASA1175",
        "ident_icao": "ASA1175",
        "ident_iata": "AS1175",
        "origin": {
            "code": "KSFO",
            "city": "San Francisco"
        },
        "destination": {
            "code": "KSEA",
            "city": "Seattle"
        },
        "last_position": {
            "altitude_change": "C"
        },
        "aircraft_type": "B739"
    },
    {
        "ident": "UAL200",
        "ident_icao": "UAL200",
        "ident_iata": "UA200",
        "origin": {
            "code": "KDEN",
            "city": "Denver"
        },
        "destination": {
            "code": "KSFO",
            "city": "San Francisco"
        },
        "last_position": {
            "altitude_change": "D"
        },
        "aircraft_type": "B738"
    },
    {
        "ident": "FFT1234",
        "ident_icao": "FFT1234",
        "ident_iata": "F91234",
        "origin": {
            "code": "KLAX",
            "city": "Los Angeles"
        },
        "destination": {
            "code": "KSJC",
            "city": "San Jose"
        },
        "last_position": {
            "altitude_change": None
        },
        "aircraft_type": "A320"
    }
]

# --- Helper for icon ---
def get_flight_icon(altitude_change):
    if altitude_change == "C":
        return "🛫"  # takeoff
    elif altitude_change == "D":
        return "🛬"  # landing
    else:
        return ""

# --- Streamlit UI ---
st.set_page_config(page_title="Flight Card Prototype", layout="centered")
st.title("Flight Data")

# Loading indicator
with st.spinner("Loading flight data..."):
    sleep(1)  # Simulate loading

# Error simulation (set to True to show error)
show_error = False
if show_error:
    st.error("Error loading flight data: Invalid API key. Please check your internet connection or API key.")
else:
    # Card container
    for flight in SAMPLE_FLIGHTS:
        # Determine which city to display (origin or destination)
        origin_code = flight.get("origin", {}).get("code")
        destination_code = flight.get("destination", {}).get("code")
        origin_city = flight.get("origin", {}).get("city", "N/A")
        destination_city = flight.get("destination", {}).get("city", "N/A")
        # Logic to display city based on SFO (as in your JS)
        if origin_code == "KSFO":
            city_display = destination_city
        elif destination_code == "KSFO":
            city_display = origin_city
        else:
            city_display = destination_city
        # Icon
        icon = get_flight_icon(flight.get("last_position", {}).get("altitude_change"))
        # Airline and aircraft type
        ident_prefix = flight["ident"][:3]
        airline_name = AIRLINE_CODES.get(ident_prefix, ident_prefix)
        flight_number = flight.get("ident_iata", "N/A").lstrip(ident_prefix) if flight.get("ident_iata") else "N/A"
        aircraft_type_code = flight.get("aircraft_type", "N/A")
        aircraft_type = AIRCRAFT_TYPES.get(aircraft_type_code, aircraft_type_code)
        # Card HTML
        st.markdown(f'''
        <div style="width:100%; max-width:400px; background:#fff; border-radius:16px; box-shadow:0 2px 8px #0001; padding:24px; border:1px solid #e5e7eb; margin-bottom:24px;">
            <div style="font-size:2rem; font-weight:600; color:#1f2937; margin-bottom:8px; display:flex; align-items:center;">
                <span style="margin-right:12px; animation:softBlink 1s infinite alternate;">{icon}</span>
                {city_display}
            </div>
            <div style="font-size:1.1rem; color:#374151; margin-bottom:4px;">{airline_name} {flight_number}</div>
            <div style="font-size:1rem; color:#6b7280;">{aircraft_type}</div>
        </div>
        <style>
        @keyframes softBlink {{ 0% {{ opacity: 1; }} 100% {{ opacity: 0.2; }} }}
        </style>
        ''', unsafe_allow_html=True)
    if not SAMPLE_FLIGHTS:
        st.info("Clear skies!")
