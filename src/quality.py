"""
Contrôles de qualité des données — volontairement simples et lisibles.
Pour une version plus poussée : remplacer par Great Expectations ou Soda Core.
"""
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class QualityReport:
    issues: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.issues) == 0

    def add(self, message: str) -> None:
        self.issues.append(message)


def check_no_nulls(df: pd.DataFrame, columns: list[str], report: QualityReport) -> None:
    for col in columns:
        n_nulls = df[col].isna().sum()
        if n_nulls > 0:
            report.add(f"'{col}' contient {n_nulls} valeur(s) nulle(s)")


def check_range(df: pd.DataFrame, column: str, min_val: float, max_val: float, report: QualityReport) -> None:
    out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]
    if len(out_of_range) > 0:
        report.add(f"'{column}' a {len(out_of_range)} valeur(s) hors de [{min_val}, {max_val}]")


def check_coherence(df: pd.DataFrame, report: QualityReport) -> None:
    """Vérifie que temp_max >= temp_min sur chaque ligne."""
    incoherent = df[df["temp_max"] < df["temp_min"]]
    if len(incoherent) > 0:
        report.add(f"{len(incoherent)} ligne(s) où temp_max < temp_min")


def run_quality_checks(df: pd.DataFrame) -> QualityReport:
    report = QualityReport()
    check_no_nulls(df, ["date", "temp_max", "temp_min"], report)
    check_range(df, "temp_max", -30, 55, report)
    check_range(df, "temp_min", -30, 55, report)
    check_range(df, "precipitation_sum", 0, 500, report)
    check_coherence(df, report)
    return report