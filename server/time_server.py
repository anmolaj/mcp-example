from fastapi import FastAPI
from datetime import datetime
import pytz

app = FastAPI(
    title="Time MCP Server",
    description="A basic MCP-compatible server for getting current time in any timezone",
    version="1.0.0"
)

# ----- MCP Tool Endpoint -----
@app.get("/time")
def get_time(timezone: str = "UTC"):
    """
    Get the current date & time for the given timezone.
    Example: /time?timezone=Asia/Kolkata
    """
    print(f"Received /time request with timezone: {timezone}")
    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        print(f"Unknown timezone requested: {timezone}")
        return {"error": f"Unknown timezone: {timezone}"}

    now = datetime.now(tz)
    result = {
        "timezone": timezone,
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "iso": now.isoformat()
    }
    print(f"Returning time result: {result}")
    return result

# ----- MCP Metadata Endpoint -----
@app.get("/mcp/metadata")
def mcp_metadata():
    """
    MCP metadata describing available tools.
    """
    print("Received /mcp/metadata request")
    metadata = {
        "mcp_version": "1.0",
        "name": "time-mcp-server",
        "description": "Returns current date & time in a given timezone",
        "tools": [
            {
                "name": "time",
                "description": "Get current date & time for a given timezone",
                "parameters": {
                    "timezone": "Name of the timezone (e.g., UTC, Asia/Kolkata)"
                }
            }
        ]
    }
    print(f"Returning metadata: {metadata}")
    return metadata

# ----- Optional root path -----
@app.get("/")
def root():
    print("Received / (root) request")
    root_info = {
        "message": "Time MCP Server is running",
        "endpoints": ["/time", "/mcp/metadata"]
    }
    print(f"Returning root info: {root_info}")
    return root_info
