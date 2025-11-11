#!/usr/bin/env python3
"""
FastMCP Weather Server
A simple weather MCP server with mock data
"""

import json
import os
from datetime import datetime, timedelta
import random
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Weather")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city
    
    Args:
        city: Name of the city (e.g., 'London', 'Tokyo', 'New York')
    """
    temp = random.randint(15, 30)
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
    
    weather = {
        "city": city,
        "temperature": f"{temp}°C",
        "condition": random.choice(conditions),
        "humidity": f"{random.randint(40, 80)}%",
        "wind": f"{random.randint(5, 25)} km/h",
        "timestamp": datetime.now().isoformat()
    }
    
    return json.dumps(weather, indent=2)

@mcp.tool()
def get_forecast(city: str, days: int = 3) -> str:
    """Get weather forecast for a city
    
    Args:
        city: Name of the city
        days: Number of days (1-7, default: 3)
    """
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
    
    result = {
        "city": city,
        "forecast": forecast
    }
    
    return json.dumps(result, indent=2)

@mcp.resource("weather://cities")
def list_cities() -> str:
    """List of major cities with current weather"""
    cities = ["London", "Tokyo", "New York", "Paris", "Sydney"]
    weather_data = []
    
    for city in cities:
        weather_data.append({
            "city": city,
            "temperature": f"{random.randint(15, 30)}°C",
            "condition": random.choice(["Sunny", "Cloudy", "Rainy"])
        })
    
    return json.dumps({"cities": weather_data, "timestamp": datetime.now().isoformat()}, indent=2)

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="sse")