from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import math

app = FastAPI(title="Booking API")



services = {
    "toilet_leak_repair": {
        "name": "Toilet Leak Repair",
        "base_price": 120.0,
        "tools": ["wrench", "sealant"],
    },
    "gutter_clean": {
        "name": "Gutter Clean",
        "base_price": 180.0,
        "tools": ["ladder", "gloves"],
    },
    "ac_tune": {
        "name": "AC Tune",
        "base_price": 150.0,
        "tools": ["thermometer", "fin comb"],
    },
}

technicians = [
    {"id": "tech_1", "name": "Kyle", "lat": -33.870, "lng": 151.209, "available": True},
    {"id": "tech_2", "name": "Ava", "lat": -33.915, "lng": 151.035, "available": True},
    {"id": "tech_3", "name": "Sofia", "lat": -33.800, "lng": 151.250, "available": False},
]



class ClientLocation(BaseModel):
    lat: float
    lng: float

class BookingRequest(BaseModel):
    service_id: str
    client_location: ClientLocation
    timeslot: str
    peak_pricing: bool



def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Simple Euclidean distance in km (not exact, but enough for demo)."""
    return math.sqrt((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2) * 111  



@app.get("/")
def root():
    return {"message": "Booking API is running!"}

@app.get("/services")
def get_services():
    return services

@app.get("/technicians")
def get_technicians():
    return technicians

@app.post("/bookings")
def create_booking(request: BookingRequest):
    
    service = services.get(request.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    
    price = service["base_price"]
    if request.peak_pricing:
        price *= 1.2
    deposit = price * 0.5

    
    nearest_tech = None
    nearest_distance = float("inf")
    for tech in technicians:
        if tech["available"]:
            dist = calculate_distance(
                request.client_location.lat,
                request.client_location.lng,
                tech["lat"],
                tech["lng"],
            )
            if dist < nearest_distance:
                nearest_distance = dist
                nearest_tech = tech

    if not nearest_tech:
        raise HTTPException(status_code=400, detail="No available technicians")

    
    response = {
        "service": {
            "id": request.service_id,
            "name": service["name"],
            "base_price": service["base_price"],
        },
        "pricing": {
            "total": round(price, 2),
            "deposit": round(deposit, 2),
        },
        "assignment": {
            "technician_id": nearest_tech["id"],
            "technician_name": nearest_tech["name"],
            "distance_km": round(nearest_distance, 2),
        },
        "timeslot": request.timeslot,
        "next_actions": ["collect_deposit", "send_confirmation_sms"],
        "tools": service["tools"],
    }
    return response
