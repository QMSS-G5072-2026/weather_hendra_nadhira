"""Tests for the weather_nah2181 package (ported from QMSS G5072 Homework 6)."""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import weather_nah2181
from weather_nah2181 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)


def test_version_is_defined():
    assert isinstance(weather_nah2181.__version__, str)


# =============================================================================
# UNIT TESTS
# =============================================================================


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0),  # freezing point of water
        (100, 212.0),  # boiling point of water
        (-40, -40.0),  # the two scales meet
        (37, 98.6),  # body temperature (returns 98.60000000000001)
        (-273.15, -459.67),  # absolute zero is allowed
        (21.5, 70.7),  # a float input
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """Known Celsius values convert to the right Fahrenheit value (up to float rounding)."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("30", TypeError),  # a string is not a number
        (None, TypeError),  # missing value
        (True, TypeError),  # bools are explicitly rejected
        ([30.0], TypeError),  # a list is not a number
        (-273.16, ValueError),  # just below absolute zero
        (-1000, ValueError),  # far below absolute zero
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Non-numeric inputs raise TypeError; values below absolute zero raise ValueError."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """NaN readings are ignored in mean/min/max and counted in n_missing."""
    # Arrange
    temps = [10.0, float("nan"), 20.0, 30.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert result["mean"] == pytest.approx(20.0)
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["n_missing"] == 1


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Unsorted station readings with one missing and one implausible (999.0) temperature."""
    return pd.DataFrame(
        {
            "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
            "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
            "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
        }
    )


def test_raw_readings_fixture(raw_readings):
    """The fixture has the expected columns, 5 rows, and exactly one missing temperature."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1


# =============================================================================
# TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """NaN and 999.0 rows are dropped, temp_f is added, rows are sorted by station/date."""
    # Arrange: worked out by hand. Surviving rows are JFK 07-02 (30.0), CPK 07-01 (25.0)
    # and LGA 07-01 (28.0); sorted by station they become CPK, JFK, LGA.
    expected = pd.DataFrame(
        {
            "station": ["CPK", "JFK", "LGA"],
            "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
            "temp_c": [25.0, 30.0, 28.0],
            "temp_f": [77.0, 86.0, 82.4],
        }
    )

    # Act
    result = clean_readings(raw_readings)

    # Assert
    assert_frame_equal(result, expected)
