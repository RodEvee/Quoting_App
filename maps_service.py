# maps_service.py
import time
from typing import List, Dict, Tuple, Optional
import requests
import folium
import streamlit as st
from geopy.geocoders import Nominatim
from config import PLANTS

geolocator = Nominatim(user_agent="cemex_quoting_app_v1")


@st.cache_data(show_spinner=False)
def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """Converts a street address into (latitude, longitude) using OpenStreetMap."""
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except Exception:
        pass
    return None


@st.cache_data(show_spinner=False)
def get_plant_coordinates() -> List[Dict]:
    """Geocodes and caches all plant coordinates once."""
    plants_with_coords = []
    for p in PLANTS:
        coords = geocode_address(p["address"])
        plants_with_coords.append({**p, "coords": coords})
        time.sleep(1.05)  # Respect Nominatim 1 req/sec rate limit on first run
    return plants_with_coords


@st.cache_data(show_spinner=False)
def rank_plants_by_distance(destination: str) -> Tuple[List[Dict], Optional[Tuple[float, float]]]:
    """Ranks all plants by driving distance using the free OSRM routing engine."""
    dest_coords = geocode_address(destination)
    if not dest_coords:
        return [], None

    plants = get_plant_coordinates()
    ranked = []

    for p in plants:
        if not p["coords"]:
            continue
        p_lat, p_lon = p["coords"]
        d_lat, d_lon = dest_coords

        url = (
            f"http://router.project-osrm.org/route/v1/driving/"
            f"{p_lon},{p_lat};{d_lon},{d_lat}?overview=full&geometries=geojson"
        )
        try:
            resp = requests.get(url, timeout=8).json()
            if resp.get("code") == "Ok":
                route = resp["routes"][0]
                miles = route["distance"] * 0.000621371
                mins = route["duration"] / 60.0
                ranked.append({
                    **p,
                    "distance_meters": route["distance"],
                    "distance_text": f"{miles:.1f} mi",
                    "duration_text": f"{int(round(mins))} mins",
                    "geometry": route["geometry"]["coordinates"],
                })
                continue
        except Exception:
            pass

        ranked.append({
            **p,
            "distance_meters": float("inf"),
            "distance_text": "N/A",
            "duration_text": "N/A",
            "geometry": [],
        })

    ranked.sort(key=lambda x: x["distance_meters"])
    return ranked, dest_coords


def build_interactive_map(selected_plant: Dict, dest_coords: Tuple[float, float], dest_label: str) -> folium.Map:
    """Creates an interactive Folium map showing the selected plant, jobsite, and driving route."""
    p_lat, p_lon = selected_plant["coords"]
    d_lat, d_lon = dest_coords

    m = folium.Map(location=[(p_lat + d_lat) / 2, (p_lon + d_lon) / 2], zoom_start=10)

    # Plant Marker (Blue)
    folium.Marker(
        [p_lat, p_lon],
        popup=f"Plant #{selected_plant['plant_number']} - {selected_plant['name']}<br>{selected_plant['address']}",
        tooltip=f"Load Plant: #{selected_plant['plant_number']} {selected_plant['name']}",
        icon=folium.Icon(color="blue", icon="industry", prefix="fa"),
    ).add_to(m)

    # Jobsite Marker (Red)
    folium.Marker(
        [d_lat, d_lon],
        popup=f"Jobsite: {dest_label}",
        tooltip="Delivery Jobsite",
        icon=folium.Icon(color="red", icon="map-pin", prefix="fa"),
    ).add_to(m)

    # Driving Route Line
    if selected_plant.get("geometry"):
        route_latlon = [[lat, lon] for lon, lat in selected_plant["geometry"]]
        folium.PolyLine(route_latlon, color="#003366", weight=5, opacity=0.85).add_to(m)
        m.fit_bounds([p_lat, p_lon], [d_lat, d_lon])

    return m