import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MCP_SERVER_URL = "http://localhost:8000"
MCP_SERVER_URL1 = "http://localhost:8001"

def ask_ollama(prompt):
    """
    Ask the LLM and get structured JSON output indicating:
      - 'use_tool': bool
      - 'tool': name (optional)
      - 'parameters': dict (optional)
      - 'answer': str (if no tool used)
    """
    system_prompt = """You are an AI agent with access to two tools:
1. 'calculate' for simple arithmetic (add, subtract, multiply, divide)
2. 'time' for getting the current date & time in any timezone

If the user request can be fulfilled by one of these tools, respond in strict JSON format:

{
  "use_tool": true/false,
  "tool": "calculate" or "time" or null,
  "parameters": { ... tool parameters ... } or null,
  "answer": "Your direct answer if no tool is needed"
}

For 'calculate', parameters must be:
{"operation": "add|subtract|multiply|divide", "a": number, "b": number}

For 'time', parameters must be:
{"timezone": "Name of timezone, e.g., UTC or Asia/Kolkata"}

Only output JSON. No text outside JSON.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gpt-oss:20b",
            "prompt": system_prompt + "\n\nUser: " + prompt,
            "options": {"temperature": 0},
            "stream": False
        }
    ).json()

    try:
        return json.loads(response["response"])
    except json.JSONDecodeError:
        print("LLM returned non-JSON output:", response["response"])
        return {"use_tool": False, "tool": None, "parameters": None, "answer": response["response"]}

def call_tool(tool, params):
    """
    Call the MCP tool endpoint with given params.
    Supports both POST and GET tools.
    """
    if tool == "time":
        resp = requests.get(f"{MCP_SERVER_URL1}/{tool}", params=params)
    else:
        resp = requests.post(f"{MCP_SERVER_URL}/{tool}", json=params)
    return resp.json()

def agent_loop(user_prompt):
    plan = ask_ollama(user_prompt)

    if plan.get("use_tool"):
        print(f"🔧 LLM decided to use tool: {plan['tool']} with params {plan['parameters']}")
        tool_result = call_tool(plan["tool"], plan["parameters"])
        
        # Give the result back to the LLM for a nice final answer
        return tool_result
        # followup_prompt = f"The tool returned this result: {tool_result}. Explain it to the user."
        # final_resp = requests.post(
        #     OLLAMA_URL,
        #     json={
        #         "model": "gpt-oss:20b",
        #         "prompt": followup_prompt,
        #         "options": {"temperature": 0},
        #         "stream": False
        #     }
        # ).json()["response"]

        # return final_resp
    else:
        print("💬 LLM answered directly without using tools.")
        return plan.get("answer", "")

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        answer = agent_loop(user_input)
        print("Agent:", answer)






# import requests
# import json

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MCP_SERVER_URL = "http://localhost:8000"

# def ask_ollama(prompt):
#     """
#     Ask the LLM and get structured JSON output indicating:
#       - 'use_tool': bool
#       - 'tool': name (optional)
#       - 'parameters': dict (optional)
#       - 'answer': str (if no tool used)
#     """
#     system_prompt = """You are an AI agent with access to a math tool.
# If the user request can be answered by simple arithmetic (add, subtract, multiply, divide),
# respond in strict JSON format:
# {
#   "use_tool": true/false,
#   "tool": "calculate" or null,
#   "parameters": {"operation": "...", "a": number, "b": number} or null,
#   "answer": "Your direct answer if no tool is needed"
# }
# Only output JSON. No text outside JSON.
# """

#     response = requests.post(
#         OLLAMA_URL,
#         json={
#             "model": "gpt-oss:20b",
#             "prompt": system_prompt + "\n\nUser: " + prompt,
#             "options": {"temperature": 0},
#             "stream": False
#         }
#     ).json()

#     try:
#         return json.loads(response["response"])
#     except json.JSONDecodeError:
#         print("LLM returned non-JSON output:", response["response"])
#         return {"use_tool": False, "tool": None, "parameters": None, "answer": response["response"]}

# def call_tool(tool, params):
#     """
#     Call the MCP tool endpoint with given params.
#     """
#     resp = requests.post(f"{MCP_SERVER_URL}/{tool}", json=params)
#     return resp.json()

# def agent_loop(user_prompt):
#     plan = ask_ollama(user_prompt)

#     if plan.get("use_tool"):
#         print(f"🔧 LLM decided to use tool: {plan['tool']} with params {plan['parameters']}")
#         tool_result = call_tool(plan["tool"], plan["parameters"])
        
#         # Give the result back to the LLM for a nice final answer
#         followup_prompt = f"The tool returned this result: {tool_result}. Explain it to the user."
#         final_resp = requests.post(
#             OLLAMA_URL,
#             json={
#                 "model": "gpt-oss:20b",
#                 "prompt": followup_prompt,
#                 "options": {"temperature": 0},
#                 "stream": False
#             }
#         ).json()["response"]

#         return final_resp
#     else:
#         print("💬 LLM answered directly without using tools.")
#         return plan.get("answer", "")

# if __name__ == "__main__":
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() in ["exit", "quit"]:
#             break
#         answer = agent_loop(user_input)
#         print("Agent:", answer)





# # import requests

# # MCP_SERVER_URL = "http://localhost:8000"

# # # Step 1: Discover tools from MCP metadata
# # metadata = requests.get(f"{MCP_SERVER_URL}/mcp/metadata").json()
# # print("MCP Metadata:", metadata)

# # # Pick the "calculate" tool
# # tool_name = "calculate"

# # # Step 2: Call the tool
# # payload = {
# #     "operation": "multiply",
# #     "a": 6,
# #     "b": 7
# # }
# # response = requests.post(f"{MCP_SERVER_URL}/{tool_name}", json=payload).json()

# # print("Tool Response:", response)

# # # Step 3 (Optional): Send the result into Ollama for natural language processing
# # ollama_resp = requests.post(
# #     "http://localhost:11434/api/generate",
# #     json={
# #         "model": "gpt-oss:20b",
# #         "prompt": f"The result of {payload['a']} {payload['operation']} {payload['b']} is {response['result']}. Explain it in words.",
# #         "options": {"temperature": 0},
# #         "stream": False
# #     }
# # ).json()

# # print("Ollama says:", ollama_resp["response"])
