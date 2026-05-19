import json

import requests

BASE_URL = "http://localhost:8001"


class HealthAgent:

    @staticmethod
    def _get(path: str):
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    @staticmethod
    def get_latest_health() -> str:
        data = HealthAgent._get("/health")
        if data is None:
            return "Eroare: API-ul nu este disponibil."
        return json.dumps(data, indent=2)

    @staticmethod
    def record_health(device_id: str, sp0: float, heartbeat: float) -> str:
        try:
            response = requests.post(
                f"{BASE_URL}/health",
                json={
                    "device_id": device_id,
                    "sp0": sp0,
                    "heartbeat": heartbeat,
                },
                timeout=5,
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except requests.RequestException as e:
            return f"Eroare la înregistrare health: {e}"

    @staticmethod
    def get_highest_heartbeat() -> dict | str:
        records = HealthAgent._get("/health")
        if records is None:
            return "Eroare: API-ul nu este disponibil."
        if not records:
            return "Nu există date de health."
        return max(records, key=lambda x: x["heartbeat"])

    @staticmethod
    def find_low_spo2(threshold: float = 92) -> list[dict]:
        records = HealthAgent._get("/health")
        if records is None:
            return []
        return [r for r in records if r["sp0"] < threshold]

    @staticmethod
    def find_high_heartbeat(threshold: float = 120) -> list[dict]:
        records = HealthAgent._get("/health")
        if records is None:
            return []
        return [r for r in records if r["heartbeat"] > threshold]
