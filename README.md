# Weather MCP Server

A simple FastMCP server that provides weather information with mock data.

## Features

- **2 Tools:**
  - `get_weather(city)` - Get current weather for a city
  - `get_forecast(city, days)` - Get weather forecast (1-7 days)

- **1 Resource:**
  - `weather://cities` - List of major cities with current weather

## Local Development

### Prerequisites
- Python 3.10 or higher

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

The server will start on `http://127.0.0.1:8000`

## Deploy to Render

1. Push this code to GitHub
2. Connect your GitHub repo to Render
3. Render will automatically use `render.yaml` for configuration
4. Your server will be live!

## Usage

This is an MCP (Model Context Protocol) server. It's designed to be used with MCP clients like:
- Claude Desktop
- Other MCP-compatible applications

### Example Tool Calls

**Get Weather:**
```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "London"
  }
}
```

**Get Forecast:**
```json
{
  "tool": "get_forecast",
  "arguments": {
    "city": "Tokyo",
    "days": 5
  }
}
```

## License

MIT
