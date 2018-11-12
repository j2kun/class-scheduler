""" A module for building and representing constraints. """

from dataclasses import dataclass
from typing import List
from typing import Set

from variables import ClassStartVariable
from variables import VariableIndexes
from data import Block
from data import Course
from data import TimeRange
from data import DayRoomTime
from data import ModelBuilderInput
from data import Room
from data import Time


class Constraint:
    def to_solver_constraint(self, solver):
        pass


@dataclass
class UniquenessConstraint:
    """ A constraint that requires every class be offered exactly once
    on the day required. """
    start_variables: Set[ClassStartVariable]


@dataclass
class ConflictConstraint:
    """ A constraint that ensures, if a class is scheduled in room r
    at time t, then no other course starts while that class is in session.

    The variable X that corresponds to the class in session is the "branching"
    variable, and the variables that may not be positive if X=1 are the
    "blocked" variables.
    """
    branching_variables: ClassStartVariable
    blocked_variables: Set[ClassStartVariable]


@dataclass
class Constraints:
    uniqueness_constraints: List[UniquenessConstraint]
    conflict_constraints: List[ConflictConstraint]

    def __len__(self):
        return (
            len(self.uniqueness_constraints)
            + len(self.conflict_constraints)
        )


def build_uniqueness_constraints(
        model_input: ModelBuilderInput,
        variable_indexes: VariableIndexes) -> List[UniquenessConstraint]:
    constraints = []

    for course in model_input.courses:
        for day in course.day_pattern:
            course_day = CourseDay(course=course, day=day)
            relevant_vars = variable_indexes.by_course_day[course_day]
            constraints.add(UniquenessConstraint(
                start_variables=relevant_vars))

    print("Built {} uniqueness constraints".format(len(constraints)))
    return constraints


def build_conflict_constraints(
        model_input: ModelBuilderInput,
        variable_indexes: VariableIndexes) -> List[ConflictConstraint]:
    constraints = []

    for class_start_var in variable_index.variables:
        course = class_start_var.course
        day = class_start_var.day
        room = class_start_var.room
        time = class_start_var.time

        day_room_time = DayRoomTime(day=day, room=room, time=time)

        relevant_vars = variable_indexes.by_day_room[]




    print("Built {} conflict constraints".format(len(constraints)))
    return constraints


def build_constraints(
        model_input: ModelBuilderInput,
        variables: VariableIndexes) -> Constraints:
    """ Build all constraints for the model. """
    uniqueness_constraints = build_uniqueness_constraints(
            model_input, variables)
    conflict_constraints = build_conflict_constraints(
            model_input, variables)

    return Constraints(
        uniqueness_constraints=uniqueness_constraints,
        conflict_constraints=conflict_constraints,
    )
