import json
import os

import ollama
from dotenv import load_dotenv

from agents.discord_agent import DiscordAgent
from agents.gps_agent import GPSAgent
from agents.health_agent import HealthAgent

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_CLIENT = ollama.Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"},
)


class Coordinator:

    def __init__(self):
        self.gps_agent = GPSAgent()
        self.health_agent = HealthAgent()
        self.discord_agent = DiscordAgent()

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

        if "alert" in q or "notifica" in q or "discord" in q:
            if "health" in q or "sanatate" in q or "puls" in q or "spo2" in q:
                return {"discord": self.discord_agent.send_health_alerts()}
            if "gps" in q or "locatie" in q:
                return {"discord": self.discord_agent.send_gps_alerts()}

            gps_data = None
            if "dispozitiv" in q or "device" in q or "locatie" in q:
                try:
                    gps_data = self.gps_agent.get_device_locations()
                except Exception:
                    pass

            if gps_data:
                lines = "\n".join(
                    f"Device {d['device_id']}: ({d['latitude']}, {d['longitude']})"
                    for d in gps_data
                )
                alert_msg = f"**Alertă dispozitive**\n{lines}"
            else:
                alert_msg = "Alertă generală de la sistemul de monitorizare."

            return {
                "discord": self.discord_agent.send_alert(alert_msg),
                "gps": gps_data,
            }

        if "device" in q or "dispozitiv" in q or "bratara" in q:
            return [d["id"] for d in self._get_devices()]

        return {
            "gps": self.gps_agent.get_device_locations(),
            "health": self.health_agent.get_latest_health(),
        }

    @staticmethod
    def _get_devices() -> list[dict]:
        import requests
        try:
            response = requests.get("http://localhost:8001/device", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

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

    print(MODEL_NAME)

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
