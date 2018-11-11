""" An internal representation of the data types needed to build the model.
"""

from datetime import time
from dataclasses import dataclass
from collections import namedtuple


class DayPattern(set):
    """A class representing a subset of the days of the week, represented as integers. """

    char_to_index = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4, }
    index_to_char = {v: k for (k, v) in char_to_index.items()}

    @staticmethod
    def parse(day_pattern_str):
        """ Build an internal representation of a day pattern from a string.

        Example: "MWR" represents "Monday, Wednesday, Thursday"
        """
        if not all(c in DayPattern.char_to_index for c in day_pattern_str):
            raise TypeError(
                ("Input {} includes invalid characters, must be a "
                 "substring of MTWRF.").format(day_pattern_str))

        return DayPattern(DayPattern.char_to_index[c] for c in day_pattern_str)

    def __repr__(self):
        return ''.join(DayPattern.index_to_char[d] for d in sorted(self))


class Time(time):
    """ A subclass of time that forces 5-minute intervals. """
    def __new__(cls, **kwargs):
        hour_minute = {
            'hour': kwargs.get('hour', 0),
            'minute': kwargs.get('minute', 0),
        }

        if hour_minute['minute'] % 5 != 0:
            raise TypeError(
                "Time must be in 5-minute increments, was {}".format(repr(kwargs)))

        return time.__new__(cls, **hour_minute)


@dataclass
class Block:
    """ A class representing a block of time. Used to make rigorous the specification
    that a course must be scheduled in the 'afternoon'.
    """
    block_id: int
    start_time: Time
    end_time: Time


@dataclass
class Course:
    """A dataclass representing a course. """
    course_id: str
    day_pattern: DayPattern
    desired_block: Block


@dataclass
class Room:
    """A dataclass representing a room. """
    room_name: str  # unique
    seats: int