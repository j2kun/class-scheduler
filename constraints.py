""" A module for building and representing constraints. """

from dataclasses import dataclass
from datetime import timedelta
from itertools import chain
from typing import List
from typing import Set

from variables import ClassStartVariable
from variables import VariableIndexes
from data import CourseDay
from data import TimeRange
from data import DayRoomTime
from data import ModelBuilderInput
from data import TimeRange


@dataclass
class UniquenessConstraint:
    """ A constraint that requires every class be offered exactly once
    on the day required. """
    start_variables: Set[ClassStartVariable]

    def to_solver_constraint(self, solver, variable_to_solver_var):
        constraint = solver.Constraint(1, 1, str(self))
        for variable in self.start_variables:
            solver_var = variable_to_solver_var[variable]
            constraint.SetCoefficient(solver_var, 1)

        return constraint

    def __str__(self):
        first_var = self.start_variables[0]
        return "Uniqueness_{}_{}".format(
            first_var.unique_class_key(),
            first_var.day,
        )


@dataclass
class ConflictConstraint:
    """ A constraint that ensures, if a class is scheduled in room r
    at time t, then no other course starts while that class is in session.

    The variable X that corresponds to the class in session is the "branching"
    variable, and the variables that may not be positive if X=1 are the
    "blocked" variables.
    """
    branching_variable: ClassStartVariable
    blocked_variables: Set[ClassStartVariable]

    def to_solver_constraint(self, solver, variable_to_solver_var):
        C = len(self.blocked_variables)
        constraint = solver.Constraint(0, C, str(self))
        branching_solver_var = variable_to_solver_var[self.branching_variable]

        constraint.SetCoefficient(branching_solver_var, C)
        for variable in self.blocked_variables:
            solver_var = variable_to_solver_var[variable]
            constraint.SetCoefficient(solver_var, 1)

        return constraint

    def __str__(self):
        branching_var = self.branching_variable
        return "Conflict_{}_{}_{}_{}".format(
            branching_var.unique_class_key(),
            branching_var.day,
            branching_var.room,
            branching_var.time,
        )


@dataclass
class Constraints:
    uniqueness_constraints: List[UniquenessConstraint]
    conflict_constraints: List[ConflictConstraint]

    def __len__(self):
        return (
            len(self.uniqueness_constraints)
            + len(self.conflict_constraints)
        )

    def all_constraints(self):
        return chain(
            self.uniqueness_constraints,
            self.conflict_constraints,
        )


def build_uniqueness_constraints(
        model_input: ModelBuilderInput,
        variable_indexes: VariableIndexes) -> List[UniquenessConstraint]:
    constraints = []

    for course in model_input.courses:
        for day in course.day_pattern:
            course_day = CourseDay(course=course, day=day)
            relevant_vars = variable_indexes.by_course_day[course_day]
            constraints.append(UniquenessConstraint(
                start_variables=relevant_vars))

    print("Built {} uniqueness constraints".format(len(constraints)))
    return constraints


def build_conflict_constraints(
        model_input: ModelBuilderInput,
        variable_indexes: VariableIndexes) -> List[ConflictConstraint]:
    constraints = []

    for class_start_var in variable_indexes.variables:
        course = class_start_var.course
        day = class_start_var.day
        room = class_start_var.room
        time = class_start_var.time

        blocked_time_range = model_input.day_range.sub_range(
            start_time=time,
            end_time=time + timedelta(minutes=course.lecture_minutes_per_day)
        )

        blocked_vars = []
        for blocked_time in blocked_time_range.values():
            day_room_time = DayRoomTime(
                day=day, room=room, time=blocked_time
            )
            blocked_vars.extend(
                variable_indexes.by_day_room_time[day_room_time]
            )

        constraints.append(ConflictConstraint(
            branching_variable=class_start_var,
            blocked_variables=blocked_vars,
        ))

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
