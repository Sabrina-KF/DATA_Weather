"""
Transformation des données météo brutes en données propres et enrichies.
"""
import pandas as pd

from src.quality import run_quality_checks


class DataQualityError(Exception):
    """Levée quand les contrôles qualité échouent sur des critères bloquants."""


def clean_weather_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et enrichit les données météo brutes."""
    df = raw_df.copy()

    df["date"] = pd.to_datetime(df["date"])
    for col in ["temp_max", "temp_min", "precipitation_sum", "wind_speed_max"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    report = run_quality_checks(df)
    if not report.is_valid:
        raise DataQualityError(
            "Échec des contrôles qualité :\n- " + "\n- ".join(report.issues)
        )

    df["temp_range"] = df["temp_max"] - df["temp_min"]
    df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2
    df["is_rainy_day"] = df["precipitation_sum"] > 1.0

    return df.sort_values("date").reset_index(drop=True)