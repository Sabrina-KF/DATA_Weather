import pandas as pd
import pytest

from src.transform import clean_weather_data, DataQualityError


def make_raw_df():
    return pd.DataFrame({
        "date": ["2026-08-26", "2026-08-27"],
        "temp_max": [24.0, 26.0],
        "temp_min": [14.0, 15.0],
        "precipitation_sum": [0.0, 3.5],
        "wind_speed_max": [12.0, 18.0],
    })


def test_clean_weather_data_adds_derived_columns():
    df = clean_weather_data(make_raw_df())
    assert "temp_range" in df.columns
    assert "temp_avg" in df.columns
    assert "is_rainy_day" in df.columns
    assert df.loc[0, "temp_range"] == pytest.approx(10.0)
    assert df.loc[0, "temp_avg"] == pytest.approx(19.0)


def test_clean_weather_data_flags_rainy_days_correctly():
    df = clean_weather_data(make_raw_df())
    assert df.loc[0, "is_rainy_day"] == False
    assert df.loc[1, "is_rainy_day"] == True


def test_clean_weather_data_raises_on_bad_data():
    bad_df = make_raw_df()
    bad_df.loc[0, "temp_max"] = 5.0
    bad_df.loc[0, "temp_min"] = 30.0
    with pytest.raises(DataQualityError):
        clean_weather_data(bad_df)