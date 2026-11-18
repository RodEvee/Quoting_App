# maps_service.py
from typing import List, Dict
from urllib.parse import quote_plus
import googlemaps
import streamlit as st
from config import PLANTS


@st.cache_data(show_spinner=False)
def rank_plants_by_distance(api_key: str, destination: str) -> List[Dict]:
    """Queries Google Maps Distance Matrix API and sorts all plants closest-first."""
    gmaps = googlemaps.Client(key=api_key)
    origins = [p["address"] for p in PLANTS]

    matrix = gmaps.distance_matrix(
        origins=origins,
        destinations=[destination],
        mode="driving",
        units="imperial",
    )

    ranked = []
    for idx, plant in enumerate(PLANTS):
        element = matrix["rows"][idx]["elements"][0]
        if element.get("status") == "OK":
            ranked.append({
                **plant,
                "distance_meters": element["distance"]["value"],
                "distance_text": element["distance"]["text"],
                "duration_text": element["duration"]["text"],
            })
        else:
            ranked.append({
                **plant,
                "distance_meters": float("inf"),
                "distance_text": "N/A",
                "duration_text": "N/A",
            })

    ranked.sort(key=lambda x: x["distance_meters"])
    return ranked


def get_directions_iframe_html(api_key: str, origin: str, destination: str) -> str:
    """Builds an interactive Google Maps Directions iframe."""
    origin_enc = quote_plus(origin)
    dest_enc = quote_plus(destination)
    return f"""
    <iframe
      width="100%"
      height="400"
      style="border:0; border-radius: 8px;"
      loading="lazy"
      allowfullscreen
      referrerpolicy="no-referrer-when-downgrade"
      src="https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={origin_enc}&destination={dest_enc}&mode=driving">
    </iframe>
    """