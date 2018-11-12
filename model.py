""" Build the course scheduler module.

Uses the MIP solver detailed at
https://developers.google.com/optimization/mip/integer_opt
"""

from data import DayRange
from data import ModelBuilderInput
from data import Time
from fetch import fetch_and_convert_data
from variables import build_variables
from constraints import build_constraints


def build_day_range():
    start_time = Time(hour=7, minute=0)  # 7:00 AM
    end_time = Time(hour=20, minute=30)  # 8:30 PM

    return DayRange(
        start_time=start_time,
        end_time=end_time,
        increment_minutes=5
    )

def build_model(model_input: ModelBuilderInput):
    """ Build the course scheduler model. """
    day_range = build_day_range()
    variables = build_variables(model_input, day_range)
    constraints = build_constraints(model_input, variables)
    pass


if __name__ == "__main__":
    model_input = fetch_and_convert_data()
    model = build_model(model_input)
