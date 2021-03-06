""" A module for building and representing the variables for the class
scheduler model.
"""
from collections import defaultdict
from dataclasses import dataclass
from itertools import product

from data import Block
from data import Course
from data import CourseDay
from data import DayRoomTime
from data import ModelBuilderInput
from data import Room
from data import Time
from data import TimeRange


class Variable:
    def to_solver_var(self, solver):
        return solver.IntVar(self.min(), self.max(), str(self))


@dataclass(eq=True, frozen=True)
class ClassStartVariable(Variable):
    """ A binary variable indexed by

    Course c
    Day (str) d
    Time t
    Room r

    which is 1 if and only if Course c on Day d starts at Time
    t in Room r.
    """
    course: Course
    day: str
    time: Time
    room: Room

    def min(self):
        return 0

    def max(self):
        return 1

    def unique_class_key(self):
        return "{}-{}-{}".format(
            self.course.course_id,
            self.course.course_name,
            self.course.day_pattern,
        )

    def __str__(self):
        return "ClassStart_{}_{}_{}_Room_{}".format(
            self.unique_class_key(),
            self.day,
            self.time,
            self.room.room_name)


class VariableIndexes:
    def __init__(self):
        self.variables = set()
        self.by_course_day = defaultdict(list)
        self.by_day_room_time = defaultdict(list)

    def __len__(self):
        return len(self.variables)

    def __iter__(self):
        return iter(self.variables)

    def add(self, variable: ClassStartVariable):
        course_day = CourseDay(course=variable.course, day=variable.day)
        day_room_time = DayRoomTime(
            day=variable.day, room=variable.room, time=variable.time
        )

        self.by_course_day[course_day].append(variable)
        self.by_day_room_time[day_room_time].append(variable)
        self.variables.add(variable)


def build_variables(model_input: ModelBuilderInput) -> VariableIndexes:
    variable_indexes = VariableIndexes()
    blocks_by_id = {b.block_id: b for b in model_input.blocks}

    for course in model_input.courses:
        block = blocks_by_id[course.desired_block]
        legal_rooms = [
            room for room in model_input.rooms if room.can_fit(course)]
        legal_times = [
            time for time in model_input.day_range.values()
            if block.contains(time)
        ]
        room_times = list(product(legal_rooms, legal_times))
        print("Generating {} variables for course='{}' days={} block={}".format(
            len(room_times),
            course.course_id,
            course.day_pattern,
            course.desired_block))

        if not room_times:
            raise ValueError("No legal room/time for {}".format(course))

        for (room, time) in room_times:
            for day in course.day_pattern:
                variable = ClassStartVariable(
                    course=course, day=day, time=time, room=room,
                )
                variable_indexes.add(variable)

    print("Created {} class start variables".format(len(variable_indexes)))
    return variable_indexes
