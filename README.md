# weather_nah2181

[![ci](https://github.com/QMSS-G5072-2026/weather_hendra_nadhira/actions/workflows/ci.yml/badge.svg)](https://github.com/QMSS-G5072-2026/weather_hendra_nadhira/actions/workflows/ci.yml)

Small utilities for converting, summarizing, and cleaning temperature readings.

## Installation

```bash
$ uv add weather_nah2181
```

or, without uv, `pip install weather_nah2181`.

## Development

```bash
$ uv sync                       # create .venv and install the package with its dev and docs groups
$ uv run pytest                 # run the tests
$ uv run make html -C docs      # build the documentation
$ uv build                      # build the sdist and wheel into dist/
```

## Usage

```python
import pandas as pd
import weather_nah2181

weather_nah2181.celsius_to_fahrenheit(25)               # 77.0
weather_nah2181.summarize_temperatures([10.0, float("nan"), 20.0])
# {'mean': 15.0, 'min': 10.0, 'max': 20.0, 'n_missing': 1}

raw = pd.DataFrame({"station": ["JFK", "CPK"], "date": ["2026-07-01"] * 2,
                    "temp_c": [30.0, float("nan")]})
weather_nah2181.clean_readings(raw)                       # drops the NaN row, adds temp_f
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`weather_nah2181` was created by Nadhira Azzahra Hendra. It is licensed under the terms of the MIT license.

## Credits

`weather_nah2181` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `qmss-pkgs-cookiecutter` [template](https://github.com/QMSS-G5072-2026/qmss-pkgs-cookiecutter), a uv-based fork of [`py-pkgs-cookiecutter`](https://github.com/py-pkgs/py-pkgs-cookiecutter).
