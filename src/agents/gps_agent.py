import json

import requests

BASE_URL = "http://localhost:8000"


class GPSAgent:

    @staticmethod
    def get_latest_gps() -> str:
        response = requests.get(f"{BASE_URL}/gps")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)

    @staticmethod
    def record_gps(device_id: str, latitude: float, longitude: float) -> str:
        response = requests.post(
            f"{BASE_URL}/gps",
            json={
                "device_id": device_id,
                "latitude": latitude,
                "longitude": longitude,
            },
        )
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)

    @staticmethod
    def get_device_locations() -> list[dict]:
        response = requests.get(f"{BASE_URL}/gps")
        response.raise_for_status()
        return response.json()
