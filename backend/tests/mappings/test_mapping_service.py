import pytest
import pandas as pd
from src.sports.hockey.mappings.standardized_names import InternalStat
from src.sports.hockey.mappings.mapping_service import MappingService
from src.sports.hockey.adapters.quant_hockey_adapter import QuantHockeyAdapter
from src.sports.hockey.adapters.hockey_reference_adapter import HockeyReferenceAdapter


class TestMappingService:
    @pytest.fixture
    def quant_adapter(self):
        return QuantHockeyAdapter()

    @pytest.fixture
    def ref_adapter(self):
        return HockeyReferenceAdapter()

    def test_normalize_columns_quant_full_spectrum(self, quant_adapter):
        """
        Tests that QuantHockey raw headers (including physical/adj stats)
        are correctly mapped to internal snake_case without data loss.
        """
        raw_data = {
            "Date": ["2026-02-01"],
            "Opponent": ["NY Rangers"],
            "GF": [4],
            "GA": [2],
            "HITS": [25],
            "HITS-A": [18],  # Opponent Hits
            "BS": [12],
            "BS-A": [15],  # Opponent Blocks
            "PDO-A": [101.5],  # Adjusted PDO
        }
        df = pd.DataFrame(raw_data)

        normalized_df = MappingService.normalize_columns(df, quant_adapter)

        # Verify renaming
        assert InternalStat.DATE.value in normalized_df.columns
        assert InternalStat.HITS.value in normalized_df.columns
        assert InternalStat.HITS_AGAINST.value in normalized_df.columns
        assert InternalStat.BLOCKS_AGAINST.value in normalized_df.columns
        assert InternalStat.PDO_ADJ.value in normalized_df.columns

        # Verify data preservation
        assert normalized_df[InternalStat.HITS_AGAINST.value].iloc[0] == 18
        assert normalized_df[InternalStat.PDO_ADJ.value].iloc[0] == 101.5

    def test_normalize_columns_hockey_reference(self, ref_adapter):
        """Tests that Hockey Reference shorthand (S, SA) maps correctly."""
        raw_data = {
            "Date": ["2026-02-01"],
            "S": [35],  # Shots For
            "SA": [28],  # Shots Against
            "SV%": [0.925],
        }
        df = pd.DataFrame(raw_data)

        normalized_df = MappingService.normalize_columns(df, ref_adapter)

        assert InternalStat.SHOTS_FOR.value in normalized_df.columns
        assert InternalStat.SHOTS_AGAINST.value in normalized_df.columns
        assert normalized_df[InternalStat.SHOTS_FOR.value].iloc[0] == 35

    def test_get_display_columns_restoration(self):
        """
        Ensures internal snake_case keys are flipped to
        print-friendly names for the UI.
        """
        internal_df = pd.DataFrame(
            {
                "date": ["2026-02-01"],
                "goals_for": [5],
                "hits_against": [20],
                "pdo_adjusted": [102.1],
            }
        )

        display_df = MappingService.get_display_columns(internal_df)

        # Check specific print-friendly titles from your requirement
        assert "Date" in display_df.columns
        assert "Goals For" in display_df.columns
        assert "Opp. Hits" in display_df.columns
        assert "Adj. PDO" in display_df.columns

    @pytest.mark.parametrize(
        "result_str, expected_points",
        [
            ("W", 2),
            ("W (OT)", 2),
            ("W-SO", 2),
            ("OTL", 1),
            ("L-SO", 1),
            ("L", 0),
            ("", 0),
            (None, 0),
        ],
    )
    def test_scoring_logic(self, result_str, expected_points):
        """Verifies points calculation from various result string formats."""
        points = MappingService.get_points_from_result(result_str)
        assert points == expected_points

    def test_team_name_lookup(self):
        """Ensures abbreviations resolve to full names correctly."""
        assert MappingService.get_full_team_name("PIT") == "Pittsburgh Penguins"
        assert MappingService.get_full_team_name("UTA") == "Utah Hockey Club"
        # Ensure it returns the input if not found instead of crashing
        assert MappingService.get_full_team_name("NON-EXISTENT") == "NON-EXISTENT"

    def test_finalize_sorting_and_ordering(self, quant_adapter):
        """Tests the Adapter's finalize method (sort by date, reorder cols)."""
        df = pd.DataFrame(
            {
                "date": ["2026-02-10", "2026-02-01"],
                "opponent": ["Flyers", "Bruins"],
                "goals_for": [3, 1],
            }
        )
        # Data must be normalized (snake_case) before calling finalize
        final_df = quant_adapter.finalize(df)

        # 1. Check Sorting
        assert final_df["date"].iloc[0] == pd.Timestamp("2026-02-01")

        # 2. Check Order (date should be present in results)
        assert "date" in final_df.columns
