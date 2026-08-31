"""
Extraction des données météo pour Tours via l'API Open-Meteo.
API publique, gratuite, sans clé requise : https://open-meteo.com
"""
import pandas as pd
import requests

from src.config import LATITUDE, LONGITUDE

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_forecast(days: int = 16) -> pd.DataFrame:
    """Récupère les prévisions météo journalières pour Tours."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "timezone": "Europe/Paris",
        "forecast_days": days,
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    payload = response.json()

    daily = payload["daily"]
    df = pd.DataFrame(
        {
            "date": daily["time"],
            "temp_max": daily["temperature_2m_max"],
            "temp_min": daily["temperature_2m_min"],
            "precipitation_sum": daily["precipitation_sum"],
            "wind_speed_max": daily["wind_speed_10m_max"],
        }
    )
    return df


if __name__ == "__main__":
    df = fetch_forecast()
    print(df.head())
    print(f"\n{len(df)} lignes extraites.")