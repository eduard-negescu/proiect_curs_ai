import json

import requests

BASE_URL = "http://localhost:8000"


class HealthAgent:

    @staticmethod
    def get_latest_health() -> str:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)

    @staticmethod
    def record_health(device_id: str, sp0: float, heartbeat: float) -> str:
        response = requests.post(
            f"{BASE_URL}/health",
            json={
                "device_id": device_id,
                "sp0": sp0,
                "heartbeat": heartbeat,
            },
        )
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)

    @staticmethod
    def get_highest_heartbeat() -> dict | str:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        records = response.json()
        if not records:
            return "Nu există date de health."
        return max(records, key=lambda x: x["heartbeat"])

    @staticmethod
    def find_low_spo2(threshold: float = 92) -> list[dict]:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        return [r for r in response.json() if r["sp0"] < threshold]

    @staticmethod
    def find_high_heartbeat(threshold: float = 120) -> list[dict]:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        return [r for r in response.json() if r["heartbeat"] > threshold]
