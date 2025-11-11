#!/usr/bin/env python3
"""
FastAPI Weather Server
A simple weather API server with mock data
"""

import json
import os
from datetime import datetime, timedelta
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Weather API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "Weather API",
        "version": "1.0.0",
        "endpoints": {
            "weather": "/weather/{city}",
            "forecast": "/forecast/{city}",
            "cities": "/cities"
        }
    }

@app.get("/weather/{city}")
async def get_weather(city: str):
    """Get current weather for a city"""
    temp = random.randint(15, 30)
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
    
    return {
        "city": city,
        "temperature": f"{temp}°C",
        "condition": random.choice(conditions),
        "humidity": f"{random.randint(40, 80)}%",
        "wind": f"{random.randint(5, 25)} km/h",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/forecast/{city}")
async def get_forecast(city: str, days: int = 3):
    """Get weather forecast for a city"""
    days = max(1, min(days, 7))
    forecast = []
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        forecast.append({
            "date": date.strftime("%Y-%m-%d"),
            "day": date.strftime("%A"),
            "high": f"{random.randint(20, 30)}°C",
            "low": f"{random.randint(10, 18)}°C",
            "condition": random.choice(["Sunny", "Cloudy", "Rainy"])
        })
    
    return {
        "city": city,
        "forecast": forecast
    }

@app.get("/cities")
async def list_cities():
    """List of major cities with current weather"""
    cities = ["London", "Tokyo", "New York", "Paris", "Sydney"]
    weather_data = []
    
    for city in cities:
        weather_data.append({
            "city": city,
            "temperature": f"{random.randint(15, 30)}°C",
            "condition": random.choice(["Sunny", "Cloudy", "Rainy"])
        })
    
    return {
        "cities": weather_data,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
