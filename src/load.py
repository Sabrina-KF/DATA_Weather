"""
Chargement des données transformées dans PostgreSQL.
"""
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config import get_database_url

TABLE_NAME = "weather_tours"


def get_engine() -> Engine:
    return create_engine(get_database_url())


def load_to_postgres(df: pd.DataFrame, engine: Engine | None = None) -> int:
    """Charge le DataFrame dans PostgreSQL. Retourne le nombre de lignes écrites."""
    engine = engine or get_engine()
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    return len(df)