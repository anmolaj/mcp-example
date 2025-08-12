# mcp-example
trying out local mcp with general examples


# Server
1. cd server
2. uvicorn calculator:app --host localhost --port 8001 
3. uvicorn time_server:app --host localhost --port 8000

# Client
1. cd client
2. python mcp_client.py