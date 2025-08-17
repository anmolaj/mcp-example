import sounddevice as sd
from scipy.io.wavfile import write

import requests
import json

SERVER_URL = "http://localhost:8000/transcribe"


def ask_ollama(input_info):
    """
    Ask the LLM and get structured JSON output indicating:
      - 'use_tool': bool
      - 'tool': name (optional)
      - 'parameters': dict (optional)
      - 'answer': str (if no tool used)
    """
    system_prompt = f"""You are a food expert:
                        Convert:
                        {input_info}
                        This into calories and individual items mentioned
                        Your output should be a json and dont output anything else
                    """
    OLLAMA_URL = "http://localhost:11434/api/generate"
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gpt-oss:20b",
            "prompt": system_prompt,
            "options": {"temperature": 0},
            "stream": False
        }
    ).json()
    print(system_prompt)
    try:
        return json.loads(response["response"])
    except json.JSONDecodeError:
        print("LLM returned non-JSON output:", response["response"])
        return {"use_tool": False, "tool": None, "parameters": None, "answer": response["response"]}

def stt(voice_recording_file):
    payload = {"file_path": voice_recording_file}
    try:
        response = requests.post(SERVER_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print("Transcript:", data.get("text"))
        return data.get("text")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

    pass

if __name__ == "__main__":
    fs = 16000  # Sample rate
    seconds = 10  # Recording duration per file

    while True:
        user_input = input("Do you want to record? (y/n): ").strip().lower()
        if user_input == "y":
            print("Recording...")
            audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
            sd.wait()
            FILE_PATH="/Users/anmol/Desktop/Personal/Projects/mcp-example/nutrition-example/output.wav"
            write(FILE_PATH, fs, audio)
            print("Recording complete, transcribing...")

            answer = stt(FILE_PATH)
            print("Agent:", answer)
            print("----asing ollama---")
            print(ask_ollama(answer))
        elif user_input == "n":
            print("Exiting.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    
    