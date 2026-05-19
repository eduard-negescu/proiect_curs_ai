import json

import requests

BASE_URL = "http://localhost:8001"


class GPSAgent:

    @staticmethod
    def _get(path: str):
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    @staticmethod
    def get_latest_gps() -> str:
        data = GPSAgent._get("/gps")
        if data is None:
            return "Eroare: API-ul nu este disponibil."
        return json.dumps(data, indent=2)

    @staticmethod
    def record_gps(device_id: str, latitude: float, longitude: float) -> str:
        try:
            response = requests.post(
                f"{BASE_URL}/gps",
                json={
                    "device_id": device_id,
                    "latitude": latitude,
                    "longitude": longitude,
                },
                timeout=5,
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except requests.RequestException as e:
            return f"Eroare la înregistrare GPS: {e}"

    @staticmethod
    def get_device_locations() -> list[dict]:
        data = GPSAgent._get("/gps")
        return data if data is not None else []
