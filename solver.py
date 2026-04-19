"""GAMSPy modeli: Atama problemi (Assignment Problem)."""

from __future__ import annotations

from typing import Dict, List, Tuple

from gamspy import Container, Equation, Model, Parameter, Sense, Set, Sum, Variable, VariableType

TRAIT_ADJUSTMENTS = {
    "Lone Wolf": -15,
    "Catalyst": 12,
    "Needs Coffee": -10,
}


def trait_adjustment(employee: Dict[str, object]) -> int:
    """Keşfedilen gizli özelliğe göre beceri ayarlamasını döndürür."""
    if not employee.get("discovered", False):
        return 0
    return TRAIT_ADJUSTMENTS.get(employee.get("hidden_trait", ""), 0)


def get_gams_recommendation(
    selected_employees: Dict[str, Dict[str, object]],
    stations: List[str],
) -> Tuple[float, Dict[str, str]]:
    """GAMSPy ile optimal atamayı çözer ve skor ile atamaları döndürür."""
    employees = list(selected_employees.keys())
    if not employees or not stations:
        return 0.0, {}

    model_container = Container()
    i = Set(model_container, "i", records=employees)
    j = Set(model_container, "j", records=stations)

    skill_records = [(name, float(selected_employees[name]["skill"])) for name in employees]
    adjustment_records = [
        (name, float(trait_adjustment(selected_employees[name]))) for name in employees
    ]

    skill = Parameter(model_container, "skill", domain=i, records=skill_records)
    adjustment = Parameter(model_container, "adjustment", domain=i, records=adjustment_records)

    x = Variable(model_container, "x", domain=[i, j], type=VariableType.BINARY)
    station_fill = Equation(model_container, "station_fill", domain=j)
    employee_once = Equation(model_container, "employee_once", domain=i)

    station_fill[j] = Sum(i, x[i, j]) == 1
    employee_once[i] = Sum(j, x[i, j]) <= 1

    objective_expr = Sum((i, j), (skill[i] + adjustment[i]) * x[i, j])

    model = Model(
        model_container,
        "assignment_model",
        equations=[station_fill, employee_once],
        problem="mip",
        sense=Sense.MAX,
        objective=objective_expr,
    )
    model.solve()

    assignments: Dict[str, str] = {}
    for name in employees:
        for station in stations:
            if x.l[name, station] >= 0.5:
                assignments[station] = name

    objective_value = sum(
        float(selected_employees[employee]["skill"]) + float(trait_adjustment(selected_employees[employee]))
        for employee in assignments.values()
    )

    return objective_value, assignments
