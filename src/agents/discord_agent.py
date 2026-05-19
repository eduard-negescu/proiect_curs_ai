import os

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))


class DiscordAgent:

    @staticmethod
    def _send_via_rest(content: str):
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json={"content": content}, headers=headers)
        response.raise_for_status()

    @staticmethod
    def send_alert(message: str) -> str:
        if not TOKEN or not CHANNEL_ID:
            return "Eroare: DISCORD_BOT_TOKEN sau DISCORD_CHANNEL_ID lipsesc."
        try:
            DiscordAgent._send_via_rest(message)
            print("Message sent")
            return f"Alertă trimisă: {message[:50]}..."
        except Exception as e:
            return f"Eroare la trimiterea alertei: {e}"

    @staticmethod
    def send_health_alerts() -> str:
        response = requests.get("http://localhost:8000/health")
        response.raise_for_status()
        records = response.json()

        alerts = []
        for r in records:
            if r["heartbeat"] > 120:
                alerts.append(
                    f"Puls ridicat: device {r['device_id']} - {r['heartbeat']} bpm"
                )
            if r["sp0"] < 92:
                alerts.append(
                    f"Saturație scăzută: device {r['device_id']} - {r['sp0']}%"
                )

        if not alerts:
            msg = "Nu există alerte de sănătate."
        else:
            msg = "**Alerte Sănătate**\n" + "\n".join(alerts)

        return DiscordAgent.send_alert(msg)

    @staticmethod
    def send_gps_alerts() -> str:
        response = requests.get("http://localhost:8000/gps")
        response.raise_for_status()
        records = response.json()

        msg = "**Locații curente**\n" + "\n".join(
            f"Device {r['device_id']}: {r['latitude']}, {r['longitude']}"
            for r in records
        ) if records else "Nu există date GPS."

        return DiscordAgent.send_alert(msg)
