#!/usr/bin/env python3
"""
MCP Weather Server for ServiceNow
Implements MCP JSON-RPC protocol over HTTP
"""

import json
import os
from datetime import datetime, timedelta
import random
from typing import Any, Dict
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

# Weather tools implementation
def get_weather_data(city: str) -> dict:
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

def get_forecast_data(city: str, days: int = 3) -> dict:
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

def get_cities_data() -> dict:
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

# MCP Protocol Handler
class MCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Name of the city"
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "get_forecast",
                "description": "Get weather forecast for a city",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Name of the city"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days (1-7)",
                            "default": 3
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
        
        self.resources = [
            {
                "uri": "weather://cities",
                "name": "Cities Weather",
                "description": "List of major cities with current weather",
                "mimeType": "application/json"
            }
        ]
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {
                        "tools": {},
                        "resources": {}
                    },
                    "serverInfo": {
                        "name": "Weather MCP Server",
                        "version": "1.0.0"
                    }
                }
            
            elif method == "tools/list":
                result = {"tools": self.tools}
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "get_weather":
                    data = get_weather_data(arguments.get("city"))
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(data, indent=2)
                            }
                        ]
                    }
                
                elif tool_name == "get_forecast":
                    data = get_forecast_data(
                        arguments.get("city"),
                        arguments.get("days", 3)
                    )
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(data, indent=2)
                            }
                        ]
                    }
                
                else:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Tool not found: {tool_name}"
                        },
                        "id": request_id
                    }
            
            elif method == "resources/list":
                result = {"resources": self.resources}
            
            elif method == "resources/read":
                uri = params.get("uri")
                if uri == "weather://cities":
                    data = get_cities_data()
                    result = {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": json.dumps(data, indent=2)
                            }
                        ]
                    }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32602,
                            "message": f"Resource not found: {uri}"
                        },
                        "id": request_id
                    }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": request_id
                }
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": request_id
            }

# Create MCP server instance
mcp_server = MCPServer()

# Starlette app
async def handle_mcp_request(request):
    """Handle incoming MCP JSON-RPC requests"""
    try:
        body = await request.json()
        response = mcp_server.handle_request(body)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            },
            "id": None
        }, status_code=400)

async def health_check(request):
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "server": "Weather MCP Server",
        "version": "1.0.0"
    })

app = Starlette(
    routes=[
        Route("/", handle_mcp_request, methods=["POST"]),
        Route("/health", health_check, methods=["GET"]),
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
