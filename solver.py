"""GAMSPy modeli: Uzmanlık + sinerji kısıtlı atama."""

from __future__ import annotations

from typing import Dict, List, Tuple

from gamspy import Container, Equation, Model, Parameter, Sense, Set, Sum, Variable, VariableType

DEPT_A_MIN_TECH = 70
DEPT_B_MIN_ANALYSIS = 60
MIN_TEAMWORK_AVG = 70


def get_gams_recommendation(
    selected_employees: Dict[str, Dict[str, object]],
    departments: List[str],
) -> Tuple[float, Dict[str, str], bool]:
    """GAMSPy ile optimal atamayı çözer ve skor/atama/uygunluk döndürür."""
    employees = list(selected_employees.keys())
    if not employees or len(departments) < 2:
        return 0.0, {}, False

    dept_a = departments[0]
    dept_b = departments[1]

    eligible_a = [
        name for name in employees if int(selected_employees[name]["skill"]) >= DEPT_A_MIN_TECH
    ]
    eligible_b = [
        name
        for name in employees
        if int(selected_employees[name]["analysis"]) >= DEPT_B_MIN_ANALYSIS
    ]
    if not eligible_a or not eligible_b:
        return 0.0, {}, False

    model_container = Container()
    i = Set(model_container, "i", records=employees)
    j = Set(model_container, "j", records=[dept_a, dept_b])

    tech = Parameter(
        model_container,
        "tech",
        domain=i,
        records=[(name, float(selected_employees[name]["skill"])) for name in employees],
    )
    analysis = Parameter(
        model_container,
        "analysis",
        domain=i,
        records=[(name, float(selected_employees[name]["analysis"])) for name in employees],
    )
    teamwork = Parameter(
        model_container,
        "teamwork",
        domain=i,
        records=[(name, float(selected_employees[name]["teamwork"])) for name in employees],
    )

    base_records = []
    eligible_records = []
    for name in employees:
        for dept in [dept_a, dept_b]:
            if dept == dept_a:
                base = float(selected_employees[name]["skill"])
                eligible = 1 if name in eligible_a else 0
            else:
                base = float(selected_employees[name]["analysis"])
                eligible = 1 if name in eligible_b else 0
            base_records.append((name, dept, base))
            eligible_records.append((name, dept, eligible))

    base_score = Parameter(model_container, "base_score", domain=[i, j], records=base_records)
    eligible = Parameter(model_container, "eligible", domain=[i, j], records=eligible_records)

    x = Variable(model_container, "x", domain=[i, j], type=VariableType.BINARY)
    dept_fill = Equation(model_container, "dept_fill", domain=j)
    emp_once = Equation(model_container, "emp_once", domain=i)
    allow = Equation(model_container, "allow", domain=[i, j])
    synergy = Equation(model_container, "synergy")

    dept_fill[j] = Sum(i, x[i, j]) == 1
    emp_once[i] = Sum(j, x[i, j]) <= 1
    allow[i, j] = x[i, j] <= eligible[i, j]
    synergy[...] = Sum((i, j), teamwork[i] * x[i, j]) >= MIN_TEAMWORK_AVG * Sum((i, j), x[i, j])

    objective_expr = Sum((i, j), base_score[i, j] * x[i, j])

    model = Model(
        model_container,
        "dept_assignment",
        equations=[dept_fill, emp_once, allow, synergy],
        problem="mip",
        sense=Sense.MAX,
        objective=objective_expr,
    )
    model.solve()

    assignments: Dict[str, str] = {dept_a: "", dept_b: ""}
    records = x.l.records
    if records is not None and not records.empty:
        for name, dept, value in records.itertuples(index=False, name=None):
            if float(value) >= 0.5:
                assignments[str(dept)] = str(name)

    if not assignments[dept_a] or not assignments[dept_b]:
        return 0.0, {}, False

    objective_value = 0.0
    if assignments[dept_a]:
        objective_value += float(selected_employees[assignments[dept_a]]["skill"])
    if assignments[dept_b]:
        objective_value += float(selected_employees[assignments[dept_b]]["analysis"])
    return objective_value, assignments, True
