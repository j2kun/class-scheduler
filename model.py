""" Build the course scheduler module.

Uses the MIP solver detailed at
https://developers.google.com/optimization/mip/integer_opt
"""
from ortools.linear_solver import pywraplp

from data import ModelBuilderInput
from fetch import fetch_and_convert_data
from variables import build_variables
from constraints import build_constraints
from timer import Timer


def build_model(model_input: ModelBuilderInput):
    """ Build the course scheduler model. """
    with Timer("Building internal representation"):
        variables = build_variables(model_input)
        constraints = build_constraints(model_input, variables)

    with Timer("Converting to ortools model"):
        solver = pywraplp.Solver(
            'SolveIntegerProblem',
            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
        )

        variable_to_solver_var = {
            var: var.to_solver_var(solver) for var in variables
        }

        for constraint in constraints.all_constraints():
            constraint.to_solver_constraint(solver, variable_to_solver_var)

        objective = solver.Objective()
        objective.SetMaximization()

    with Timer("Soving model"):
        result_status = solver.Solve()

    print("Finished solve, status={}.".format(result_status))

    sorted_variables = sorted(
        variable_to_solver_var.values(), key=lambda v: v.name())
    for variable in sorted_variables:
        if variable.solution_value() > 0:
            print('%s = %d' % (variable.name(), variable.solution_value()))


if __name__ == "__main__":
    model_input = fetch_and_convert_data()
    model = build_model(model_input)
