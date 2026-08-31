import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import get_database_url
from src.load import TABLE_NAME

st.set_page_config(page_title="Météo Tours — Pipeline ELT", layout="wide")
st.title("🌦️ Prévisions météo — Tours")
st.caption("Données extraites via Open-Meteo, transformées et orchestrées avec Dagster.")

engine = create_engine(get_database_url())

try:
    df = pd.read_sql_table(TABLE_NAME, engine)
except Exception as e:
    st.error(
        "Impossible de lire les données. As-tu lancé le pipeline Dagster au moins une fois ? "
        f"(détail : {e})"
    )
    st.stop()

df["date"] = pd.to_datetime(df["date"])

col1, col2, col3 = st.columns(3)
col1.metric("Température moyenne", f"{df['temp_avg'].mean():.1f} °C")
col2.metric("Jours de pluie prévus", int(df["is_rainy_day"].sum()))
col3.metric("Vent max prévu", f"{df['wind_speed_max'].max():.0f} km/h")

st.subheader("Températures min / max par jour")
st.line_chart(df.set_index("date")[["temp_min", "temp_max"]])

st.subheader("Précipitations prévues (mm)")
st.bar_chart(df.set_index("date")["precipitation_sum"])

st.subheader("Données détaillées")
st.dataframe(df, use_container_width=True)