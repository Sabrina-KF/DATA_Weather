"""
Orchestration Dagster : chaque étape du pipeline est un "asset" versionné,
observable et rejouable indépendamment depuis l'interface Dagster (localhost:3000).
"""
import pandas as pd
from dagster import asset, Definitions, MaterializeResult, MetadataValue

from src.extract import fetch_forecast
from src.transform import clean_weather_data
from src.load import load_to_postgres


@asset
def raw_weather() -> pd.DataFrame:
    """Données météo brutes extraites de l'API Open-Meteo."""
    return fetch_forecast(days=16)


@asset
def clean_weather(raw_weather: pd.DataFrame) -> pd.DataFrame:
    """Données météo nettoyées, enrichies et validées."""
    return clean_weather_data(raw_weather)


@asset
def weather_in_db(clean_weather: pd.DataFrame) -> MaterializeResult:
    """Écriture finale en base PostgreSQL, consommée ensuite par le dashboard."""
    n_rows = load_to_postgres(clean_weather)
    return MaterializeResult(
        metadata={
            "n_rows": MetadataValue.int(n_rows),
            "preview": MetadataValue.md(clean_weather.head().to_markdown()),
        }
    )


defs = Definitions(assets=[raw_weather, clean_weather, weather_in_db])