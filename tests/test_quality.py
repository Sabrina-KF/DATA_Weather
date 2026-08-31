import pandas as pd

from src.quality import run_quality_checks


def test_valid_data_passes():
    df = pd.DataFrame({
        "date": ["2026-08-26", "2026-08-27"],
        "temp_max": [24.0, 26.0],
        "temp_min": [14.0, 15.0],
        "precipitation_sum": [0.0, 2.5],
    })
    report = run_quality_checks(df)
    assert report.is_valid


def test_detects_incoherent_temperatures():
    df = pd.DataFrame({
        "date": ["2026-08-26"],
        "temp_max": [10.0],
        "temp_min": [20.0],
        "precipitation_sum": [0.0],
    })
    report = run_quality_checks(df)
    assert not report.is_valid
    assert any("temp_max < temp_min" in issue for issue in report.issues)


def test_detects_out_of_range_values():
    df = pd.DataFrame({
        "date": ["2026-08-26"],
        "temp_max": [999.0],
        "temp_min": [15.0],
        "precipitation_sum": [0.0],
    })
    report = run_quality_checks(df)
    assert not report.is_valid