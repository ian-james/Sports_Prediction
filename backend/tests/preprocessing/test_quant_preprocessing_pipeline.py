from pathlib import Path

import pandas as pd
import pytest
from bs4 import BeautifulSoup

from src.helpers.file_helpers import load_read_file
from src.sports.hockey.adapters.quant_hockey_adapter import QuantHockeyAdapter
from src.sports.hockey.mappings.mapping_service import MappingService
from src.sports.hockey.mappings.standardized_names import InternalStat
from src.sports.hockey.parsers.QuantHockeyParser import QuantHockeyParser
from src.sports.hockey.preprocessing.quant_preprocessing_pipeline import (
    handle_missing_data,
    normalize_dates,
    normalize_location,
    normalize_outcomes,
    preprocess,
)


def _make_df(**kwargs) -> pd.DataFrame:
    """Builds a minimal post-finalize()-style DataFrame for unit tests."""
    n = len(next(iter(kwargs.values()))) if kwargs else 2
    base = {
        InternalStat.DATE.value: pd.date_range("2025-10-01", periods=n, freq="2D"),
        InternalStat.RESULT.value: ["Win"] * n,
        InternalStat.IS_HOME.value: [True] * n,
        InternalStat.WON.value: [True] * n,
        InternalStat.OT_GAME.value: [False] * n,
        InternalStat.POINTS_EARNED.value: [2] * n,
        InternalStat.GOALS_FOR.value: ["3"] * n,
        InternalStat.GOALS_AGAINST.value: ["1"] * n,
    }
    base.update(kwargs)
    return pd.DataFrame(base)


@pytest.fixture
def finalized_quant_df():
    """Full pipeline fixture: parse real HTML → normalize → finalize."""
    fixture = Path(__file__).parent / ".." / "fixtures" / "Quant_Pens_2025-26.html"
    html = load_read_file(fixture.resolve())
    soup = BeautifulSoup(html, "html.parser")
    parser = QuantHockeyParser()
    adapter = QuantHockeyAdapter()
    cats = parser.parse_categories(soup)
    df = parser.parse_dataframe(soup, "Pittsburgh Penguins", cats)
    df = MappingService.normalize_columns(df, adapter)
    return adapter.finalize(df)


class TestNormalizeDates:
    def test_datetime_column_preserved(self):
        df = _make_df()
        result = normalize_dates(df)
        assert pd.api.types.is_datetime64_any_dtype(result[InternalStat.DATE.value])

    def test_string_dates_parsed(self):
        df = _make_df(**{InternalStat.DATE.value: ["2025-10-01", "2025-10-03"]})
        result = normalize_dates(df)
        assert pd.api.types.is_datetime64_any_dtype(result[InternalStat.DATE.value])
        assert len(result) == 2

    def test_unparseable_dates_dropped(self):
        df = _make_df(
            **{InternalStat.DATE.value: ["2025-10-01", "not-a-date", "2025-10-05"]}
        )
        result = normalize_dates(df)
        assert len(result) == 2


class TestNormalizeOutcomes:
    def test_valid_results_kept(self):
        df = _make_df(**{InternalStat.RESULT.value: ["Win", "Loss", "OT Loss"]})
        result = normalize_outcomes(df)
        assert len(result) == 3

    def test_null_result_rows_dropped(self):
        df = _make_df(**{InternalStat.RESULT.value: ["Win", None, "Loss"]})
        result = normalize_outcomes(df)
        assert len(result) == 2

    def test_empty_string_result_rows_dropped(self):
        df = _make_df(**{InternalStat.RESULT.value: ["Win", "", "Loss"]})
        result = normalize_outcomes(df)
        assert len(result) == 2


class TestNormalizeLocation:
    def test_is_home_coerced_to_bool(self):
        df = _make_df(**{InternalStat.IS_HOME.value: [1, 0, 1]})
        result = normalize_location(df)
        assert result[InternalStat.IS_HOME.value].dtype == bool

    def test_at_symbol_rows_are_away(self):
        df = _make_df(**{InternalStat.IS_HOME.value: [True, False, True]})
        result = normalize_location(df)
        assert result[InternalStat.IS_HOME.value].tolist() == [True, False, True]


class TestHandleMissingData:
    def test_string_numeric_columns_coerced_to_float(self):
        df = _make_df(**{InternalStat.GOALS_FOR.value: ["3", "+2", "-1", ""]})
        result = handle_missing_data(df)
        assert result[InternalStat.GOALS_FOR.value].dtype == float

    def test_empty_string_numeric_filled_with_zero(self):
        df = _make_df(**{InternalStat.GOALS_FOR.value: ["3", "", "2"]})
        result = handle_missing_data(df)
        assert result[InternalStat.GOALS_FOR.value].iloc[1] == 0.0

    def test_plus_prefixed_values_parsed_correctly(self):
        df = _make_df(**{InternalStat.GOAL_DIFF.value: ["+3", "-1", "+0"]})
        result = handle_missing_data(df)
        assert result[InternalStat.GOAL_DIFF.value].tolist() == [3.0, -1.0, 0.0]


class TestPreprocessFullPipeline:
    def test_output_is_nonempty(self, finalized_quant_df):
        result = preprocess(finalized_quant_df)
        assert not result.empty

    def test_date_column_is_datetime(self, finalized_quant_df):
        result = preprocess(finalized_quant_df)
        assert pd.api.types.is_datetime64_any_dtype(result[InternalStat.DATE.value])

    def test_sorted_ascending_by_date(self, finalized_quant_df):
        result = preprocess(finalized_quant_df)
        dates = result[InternalStat.DATE.value]
        assert dates.is_monotonic_increasing

    def test_goals_for_is_float(self, finalized_quant_df):
        result = preprocess(finalized_quant_df)
        assert result[InternalStat.GOALS_FOR.value].dtype == float

    def test_no_nan_in_key_columns(self, finalized_quant_df):
        result = preprocess(finalized_quant_df)
        for col in [
            InternalStat.GOALS_FOR.value,
            InternalStat.GOALS_AGAINST.value,
            InternalStat.SHOTS_FOR.value,
            InternalStat.SHOTS_AGAINST.value,
        ]:
            if col in result.columns:
                assert result[col].isna().sum() == 0, f"{col} has NaN values"

    def test_is_home_is_bool(self, finalized_quant_df):
        result = preprocess(finalized_quant_df)
        assert result[InternalStat.IS_HOME.value].dtype == bool
