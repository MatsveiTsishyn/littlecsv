
# littlecsv

[![PyPi Version](https://img.shields.io/pypi/v/littlecsv.svg)](https://pypi.org/project/littlecsv/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

`littlecsv` is a simple, lightweight `pip` package for reading, writing, and managing CSV (.csv) files in Python.

- Entries are simply represented as dictionaries: {header_property → entry_value}
- Provides only basic manipulation methods (`add_col`, `remove_col`, …) with fully explicit behaviors
- Never assumes a column or cell `type` unless explicitly specified (all cells are `str` by default)
- Strict on format: no redundant columns in the header, and each line must have the same number of elements

## Why ?

I know it’s generally considered bad practice to avoid standard tools like `pandas`, however …
The package could just as well be called `nopandas`.

Everyone uses pandas, yet few truly understand what it’s doing under the hood. This encourages a “just push the magic button” R-style workflow that I personally dislike (or maybe I just don’t like reading the docs…).

In contrast, here’s a pip package that almost no one uses (except me, sometimes) — but that anyone could understand. It’s a small, simple, and lightweight CSV/DataFrame manager that does no wild, hidden tricks — only clear, explicit manipulations.

Of course, it’s less optimized than pandas code, but in my experience, the memory or computational bottleneck rarely lies in basic data manipulation.

## Installation and Usage

Install with `pip`:
```bash
pip install littlecsv
```

You can now preview a CSV file with the command line:
```bash
littlecsv_show ./data_sample.csv
```

Here is a very brief usage example. For more, have a look to `./usage_example.py`.
```python
from littlecsv import CSV
dataset = CSV.read("./data_sample.csv")
dataset.rename_col("sec_str", "secondary structure")
dataset.write("./data_sample_renamed.csv")
```

## Requirements

- Python 3.9 or later
- Python packages `numpy`

