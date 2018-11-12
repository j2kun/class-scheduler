from assertpy import assert_that
from itertools import combinations
import pytest

from data import Time
from data import DayPattern
from data import TimeRange


def test_daypattern():
    assert_that(repr(DayPattern.parse('MWF'))).is_equal_to('MWF')


def test_daypattern_bad_day():
    with pytest.raises(TypeError):
        DayPattern.parse('MSF')


def test_daypattern_no_errors():
    all_days = 'MTWRF'
    for m in range(len(all_days)):
        for subset in combinations('MTWRF', m):
            DayPattern.parse(''.join(subset))


def test_time():
    time = Time(hour=7, minute=30)
    assert_that(time.minute).is_equal_to(30)
    assert_that(time.hour).is_equal_to(7)
    assert_that(time.second).is_equal_to(0)


def test_time_invalid_minutes():
    with pytest.raises(TypeError):
        Time(hour=7, minute=31)

def test_day_range_5_minutes():
    dr = TimeRange(start_time=Time(hour=7, minute=30), end_time=Time(hour=20, minute=30), increment_minutes=5)
    assert_that(dr.times).is_length(157)


def test_day_range_index():
    dr = TimeRange(start_time=Time(hour=7, minute=30), end_time=Time(hour=20, minute=30), increment_minutes=5)
    time = dr.times[37]
    assert_that(dr.index(time)).is_equal_to(37)
