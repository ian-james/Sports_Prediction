import pytest
import pandas as pd
from src.sports.hockey.mappings.standardized_names import InternalStat
from src.sports.hockey.adapters.quant_hockey_adapter import QuantHockeyAdapter
from src.sports.hockey.adapters.hockey_reference_adapter import HockeyReferenceAdapter
from src.sports.hockey.mappings.mapping_service import MappingService


@pytest.fixture
def sample_raw_quant_data():
    """Simulates raw data from QuantHockey including physical stats."""
    return pd.DataFrame(
        {
            "Date": ["2026-01-10"],
            "Opponent": ["NY Rangers"],
            "HITS": [25],
            "HITS-A": [18],
            "BS": [12],
            "BS-A": [15],
        }
    )


def test_quant_adapter_column_mapping(sample_raw_quant_data):
    adapter = QuantHockeyAdapter()
    normalized_df = MappingService.normalize_columns(sample_raw_quant_data, adapter)

    # Verify critical physical fields are preserved and renamed
    assert InternalStat.HITS.value in normalized_df.columns
    assert InternalStat.HITS_AGAINST.value in normalized_df.columns
    assert InternalStat.BLOCKS.value in normalized_df.columns
    assert InternalStat.BLOCKS_AGAINST.value in normalized_df.columns

    # Verify data integrity
    assert normalized_df[InternalStat.HITS_AGAINST.value].iloc[0] == 18


def test_hockey_reference_adapter_column_mapping():
    adapter = HockeyReferenceAdapter()
    raw_df = pd.DataFrame({"S": [30], "SA": [25], "SV%": [0.920]})

    normalized_df = MappingService.normalize_columns(raw_df, adapter)

    assert InternalStat.SHOTS_FOR.value in normalized_df.columns
    assert InternalStat.SHOTS_AGAINST.value in normalized_df.columns
    assert normalized_df[InternalStat.SHOTS_AGAINST.value].iloc[0] == 25
