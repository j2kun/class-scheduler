""" An internal representation of the data types needed to build the model.
"""

from dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import List


class DayPattern(str):
    """A class representing a subset of the days of the week, represented as integers. """

    valid_chars = 'MTWRF'

    @staticmethod
    def parse(day_pattern_str):
        """ Build an internal representation of a day pattern from a string.

        Example: "MWR" represents "Monday, Wednesday, Thursday"
        """
        if not all(c in DayPattern.valid_chars for c in day_pattern_str):
            raise TypeError(
                ("Input {} includes invalid characters, must be a "
                 "substring of MTWRF.").format(day_pattern_str))

        return DayPattern(''.join(
            sorted(set(day_pattern_str), key=DayPattern.valid_chars.index)
        ))


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

    def __add__(self, td: timedelta):
        """ Add a timedelta to self. """
        t = (datetime.combine(datetime.today(), self) + td).time()
        return Time(hour=t.hour, minute=t.minute)

    def add_minutes(self, minutes: int):
        return self + timedelta(minutes=minutes)

    def __str__(self):
        return "{:02d}{:02d}".format(self.hour, self.minute)

    """We must override the copy and deepcopy methods because we override
    the init/new process for this class. Doing a deepcopy of (e.g.) a dict
    that has Times as values would otherwise cause problems as the dict
    would attempt to guess at the *args signature of __init__.
    """
    def __copy__(self):
        return Time(hour=self.hour, minute=self.minute)

    def __deepcopy__(self, memo):
        return Time(hour=self.hour, minute=self.minute)


class TimeRange:
    """ A class representing a range of 5-minute intervals.

    This class exists so that each 5-minute increment can be given a unique index,
    and those indexes can be converted back and forth between human-readable dates
    and solver-readable intervals.

    Attriutes:
     - times: the list of Time objects represented in this TimeRange.
    """

    def __init__(self, start_time: Time, end_time: Time, increment_minutes: int):
        times = [start_time]
        while times[-1] < end_time:
            t = times[-1]
            times.append(t.add_minutes(increment_minutes))

        self.increment_minutes = increment_minutes
        self.times = dict(enumerate(times))
        self.time_to_index = {v: k for (k, v) in self.times.items()}

    def index(self, t: Time):
        return self.time_to_index[t]

    def items(self):
        return self.times.items()

    def values(self):
        return self.times.values()

    def sub_range(self, start_time: Time, end_time: Time):
        return TimeRange(
                start_time=start_time,
                end_time=end_time,
                increment_minutes=self.increment_minutes)


class BaseDataclass:
    """ A helper base class to make smoother dict usage. """
    def as_dict(self):
        return asdict(self)

    def items(self):
        return self.as_dict().items()

    def __iter__(self):
        return iter(self.items())


@dataclass(eq=True, frozen=True)
class Block(BaseDataclass):
    """ A class representing a block of time. Used to make rigorous the specification
    that a course must be scheduled in the 'afternoon'.
    """
    block_id: int
    start_time: Time
    end_time: Time

    def contains(self, time: Time) -> bool:
        return self.start_time < time < self.end_time


@dataclass(eq=True, frozen=True)
class Course(BaseDataclass):
    """A dataclass representing a course. """
    course_id: str
    course_name: str
    day_pattern: DayPattern
    desired_block: int
    enrollment: int
    lecture_minutes_per_day: int
    lab_minutes_per_week: int


@dataclass(eq=True, frozen=True)
class Room(BaseDataclass):
    """A dataclass representing a room. """
    room_name: str  # unique
    seats: int

    def can_fit(self, course: Course) -> bool:
        return self.seats > course.enrollment


@dataclass(eq=True, frozen=True)
class ModelBuilderInput(BaseDataclass):
    courses: List[Course]
    rooms: List[Room]
    blocks: List[Block]
    day_range: TimeRange


""" Index classes. """

@dataclass(eq=True, frozen=True)
class DayRoomTime(BaseDataclass):
    day: str
    room: Room
    time: Time


@dataclass(eq=True, frozen=True)
class CourseDay(BaseDataclass):
    course: Course
    day: str
