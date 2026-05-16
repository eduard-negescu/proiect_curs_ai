import json
import os

import ollama
from dotenv import load_dotenv

from agents.gps_agent import GPSAgent
from agents.health_agent import HealthAgent

load_dotenv()

MODEL_NAME = "gpt-oss:20b"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_CLIENT = ollama.Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"},
)


class Coordinator:

    def __init__(self):
        self.gps_agent = GPSAgent()
        self.health_agent = HealthAgent()

    def route(self, query: str):
        q = query.lower()

        if "gps" in q or "locatie" in q or "pozi" in q or "unde" in q:
            return self.gps_agent.get_device_locations()

        if "heartbeat" in q or "puls" in q or "inima" in q:
            if "mare" in q or "maxim" in q or "cel mai" in q:
                return self.health_agent.get_highest_heartbeat()
            if "ridicat" in q or "peste" in q:
                return self.health_agent.find_high_heartbeat()
            return self.health_agent.get_latest_health()

        if "spo2" in q or "oxigen" in q or "saturatie" in q:
            return self.health_agent.find_low_spo2()

        if "device" in q or "dispozitiv" in q or "bratara" in q:
            return [d["id"] for d in self._get_devices()]

        return {
            "gps": self.gps_agent.get_device_locations(),
            "health": self.health_agent.get_latest_health(),
        }

    @staticmethod
    def _get_devices() -> list[dict]:
        import requests
        response = requests.get("http://localhost:8000/device")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def generate(query: str, data) -> str:
        prompt = f"""
Ești un asistent IoT pentru brățări de monitorizare.

Ai acces la date despre:
- dispozitive (brățări)
- GPS (locații)
- health monitoring (SpO2, puls)

IMPORTANT:
- Nu inventa date.
- Folosește DOAR informațiile primite.
- Răspunde în română.
- Fii clar și concis.

Întrebare:
{query}

Date:
{json.dumps(data, indent=2, default=str)}

Răspuns:
"""
        response = OLLAMA_CLIENT.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]


def main():
    print("\n==============================")
    print(" IoT Bracelet Agent CLI")
    print("==============================\n")

    coordinator = Coordinator()

    while True:
        try:
            query = input("Întrebare > ")
        except (EOFError, KeyboardInterrupt):
            break

        if query.lower() in ("exit", "quit", "iesire"):
            break

        if not query.strip():
            continue

        try:
            data = coordinator.route(query)
            answer = coordinator.generate(query, data)
            print("\n--------------------------------")
            print(answer)
            print("--------------------------------\n")
        except Exception as e:
            print(f"\nEROARE: {e}\n")


if __name__ == "__main__":
    main()
