"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

GROUPS = ["marital_status", "qualification"]

# Assign values for c_unit
c_unit_values = (0, 0.05, 0.15, 0.4)

# Assign values for time variation
c_var_values = (0.03, 0.1, 0.25, 0.5)

# Assign values for time trend
c_trend_values = (0.03, 0.1, 0.25, 0.5)

# Assign values for c_time
c_time_values = (0, 0.015, 0.05, 0.2)

c_values = [c_unit_values, c_var_values, c_trend_values, c_time_values]

c_names = ["c_unit", "c_var", "c_trend", "c_time"]

__all__ = ["BLD", "SRC", "TEST_DIR", "GROUPS"]
