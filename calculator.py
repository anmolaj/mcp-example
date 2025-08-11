from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI(
    title="Math MCP Server",
    description="A basic MCP-compatible server exposing math operations",
    version="1.0.0"
)

# ----- Request and Response Models -----
class MathRequest(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide"]
    a: float
    b: float

class MathResponse(BaseModel):
    result: float
    operation: str

# ----- MCP Tool Endpoints -----
@app.post("/calculate", response_model=MathResponse)
def calculate(req: MathRequest):
    """
    Perform a basic math calculation based on the operation.
    """
    print(f"Received request: operation={req.operation}, a={req.a}, b={req.b}")
    if req.operation == "add":
        result = req.a + req.b
        print(f"Adding: {req.a} + {req.b} = {result}")
    elif req.operation == "subtract":
        result = req.a - req.b
        print(f"Subtracting: {req.a} - {req.b} = {result}")
    elif req.operation == "multiply":
        result = req.a * req.b
        print(f"Multiplying: {req.a} * {req.b} = {result}")
    elif req.operation == "divide":
        if req.b == 0:
            print("Error: Division by zero")
            return {"result": None, "operation": "Error: Division by zero"}
        result = req.a / req.b
        print(f"Dividing: {req.a} / {req.b} = {result}")
    else:
        print(f"Invalid operation: {req.operation}")
        return {"result": None, "operation": "Invalid Operation"}

    print(f"Returning result: {result} for operation {req.operation}")
    return {"result": result, "operation": req.operation}

# ----- MCP Metadata Endpoint -----
@app.get("/mcp/metadata")
def mcp_metadata():
    """
    MCP-required endpoint to describe available tools.
    """
    print("Metadata endpoint called")
    return {
        "mcp_version": "1.0",
        "name": "math-mcp-server",
        "description": "Performs basic math operations",
        "tools": [
            {
                "name": "calculate",
                "description": "Perform add, subtract, multiply, or divide on two numbers",
                "parameters": {
                    "operation": "One of: add, subtract, multiply, divide",
                    "a": "First number",
                    "b": "Second number"
                }
            }
        ]
    }
