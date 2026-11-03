# read version from installed package
from importlib.metadata import version

from weather_nah2181.weather_nah2181 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

__version__ = version("weather_nah2181")

__all__ = ["celsius_to_fahrenheit", "clean_readings", "summarize_temperatures"]
