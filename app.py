"""Streamlit arayüzü: The Factory Lab 🏭."""

from __future__ import annotations

import random
from typing import Dict, List, Tuple

import streamlit as st
import pandas as pd

from data import EMPLOYEE_POOL, LEVELS, discover_employee_trait
from solver import get_gams_recommendation

DEPARTMENTS = [
    "Department A (Production & Mechanical)",
    "Department B (R&D & Planning)",
]
GAMS_BLUE = "#2f81f7"
SUCCESS_GREEN = "#3fb950"


def level_total_budget(level_id: int) -> int:
    """Compute total budget for level from base or incremental definition."""
    level = LEVELS[level_id]
    base_budget = int(level.get("budget", 0))
    if level_id == 1:
        return base_budget
    increment = int(level.get("budget_increase", 0))
    if increment > 0:
        previous_budget = int(LEVELS[level_id - 1].get("budget", 0))
        return previous_budget + increment
    return base_budget


def get_recruitment_candidates(level_id: int) -> List[str]:
    """Return current candidate list shown in recruitment stage for the level."""
    level = LEVELS[level_id]
    if "recruitment_candidates_by_level" not in st.session_state:
        st.session_state.recruitment_candidates_by_level = {}
    candidate_map = st.session_state.recruitment_candidates_by_level
    if level_id not in candidate_map:
        candidate_map[level_id] = list(level["candidates"])
    return candidate_map[level_id]


def refresh_recruitment_candidates(level_id: int) -> None:
    """Refresh candidate cards with a random set from full data pool."""
    level = LEVELS[level_id]
    target_count = len(level["candidates"])
    available = [
        name
        for name in EMPLOYEE_POOL.keys()
        if name not in st.session_state.hired
    ]
    if not available:
        return
    pick_count = min(target_count, len(available))
    st.session_state.recruitment_candidates_by_level[level_id] = random.sample(
        available, pick_count
    )


def apply_dashboard_theme() -> None:
    """Endüstriyel, modern dashboard teması."""
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: #0f1115; color: #e6edf3; }}
        section[data-testid="stSidebar"] {{
            background-color: #111318;
            border-right: 1px solid #1f232a;
        }}
        .sticky-bar {{
            position: sticky;
            top: 0;
            z-index: 30;
            background: #0f1115;
            border: 1px solid #2a2d34;
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 16px;
        }}
        .sticky-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }}
        .sticky-item {{
            background: #15171c;
            border: 1px solid #2a2d34;
            border-radius: 10px;
            padding: 8px 12px;
        }}
        .muted {{ color: #8b929c; }}
        .accent {{ color: {GAMS_BLUE}; }}
        .success {{ color: {SUCCESS_GREEN}; }}
        .flip-card {{
            perspective: 1000px;
            height: 320px;
            margin-bottom: 16px;
        }}
        .flip-card-inner {{
            position: relative;
            width: 100%;
            height: 320px;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }}
        .flip-card.flipped .flip-card-inner {{
            transform: rotateY(180deg);
        }}
        .flip-card-front, .flip-card-back {{
            position: absolute;
            width: 100%;
            height: 320px;
            backface-visibility: hidden;
            background: #15171c;
            border: 1px solid #2a2d34;
            border-radius: 12px;
            padding: 14px;
        }}
        .flip-card-back {{
            transform: rotateY(180deg);
        }}
        .avatar {{
            width: 62px;
            height: 62px;
            border-radius: 50%;
            background: #1f232a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 8px;
            animation: pulse 2s infinite;
            box-shadow: 0 0 0 0 rgba(47, 129, 247, 0.6);
        }}
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(47, 129, 247, 0.6); }}
            70% {{ box-shadow: 0 0 0 10px rgba(47, 129, 247, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(47, 129, 247, 0); }}
        }}
        .progress {{
            background: #0f1115;
            border: 1px solid #2a2d34;
            height: 8px;
            border-radius: 999px;
            overflow: hidden;
        }}
        .progress-bar {{
            background: {GAMS_BLUE};
            height: 8px;
        }}
        .consultant-box {{
            background-color: #14171d;
            border: 1px solid #2a2d34;
            border-radius: 12px;
            padding: 12px 14px;
        }}
        .stButton>button {{
            background-color: {GAMS_BLUE};
            color: #ffffff;
            border: 0;
        }}
        .stButton>button:disabled {{
            background-color: #3b4250;
            color: #c9d1d9;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_state() -> None:
    """Session state başlangıcı."""
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "stage" not in st.session_state:
        st.session_state.stage = "recruitment"
    if "level_budget" not in st.session_state:
        level_id = st.session_state.level
        level = LEVELS[level_id]
        st.session_state.level_budget = (
            level_total_budget(level_id) + int(level.get("bonus_budget", 0))
        )
    if "budget" not in st.session_state:
        st.session_state.budget = st.session_state.level_budget
    if "hired" not in st.session_state:
        st.session_state.hired = []
    if "hires_at_level_start" not in st.session_state:
        st.session_state.hires_at_level_start = len(st.session_state.hired)
    if "assignments" not in st.session_state:
        st.session_state.assignments = {dept: "Select" for dept in DEPARTMENTS}
    if "consultant_message" not in st.session_state:
        st.session_state.consultant_message = "GAMS Consultant is ready."
    if "last_assignments" not in st.session_state:
        st.session_state.last_assignments = dict(st.session_state.assignments)
    if "city_health" not in st.session_state:
        st.session_state.city_health = 35.0
    if "last_city_health" not in st.session_state:
        st.session_state.last_city_health = st.session_state.city_health
    if "toast_message" not in st.session_state:
        st.session_state.toast_message = ""
    if "crisis_history" not in st.session_state:
        st.session_state.crisis_history = []
    if "performance_bonus" not in st.session_state:
        st.session_state.performance_bonus = 0
    if "last_bonus_awarded_day" not in st.session_state:
        st.session_state.last_bonus_awarded_day = 0
    if "current_crisis" not in st.session_state:
        st.session_state.current_crisis = LEVELS[st.session_state.level]["crisis_name"]
    if "level_cleared" not in st.session_state:
        st.session_state.level_cleared = False
    if "recruitment_candidates_by_level" not in st.session_state:
        st.session_state.recruitment_candidates_by_level = {}


def reset_level(level_id: int, carryover_budget: int | None = None) -> None:
    """Yeni seviyeye geçişte state resetler."""
    level = LEVELS[level_id]
    st.session_state.level = level_id
    st.session_state.stage = "recruitment"
    if level_id == 1:
        next_budget = level_total_budget(level_id)
    else:
        base_budget = (
            st.session_state.budget if carryover_budget is None else int(carryover_budget)
        )
        next_budget = base_budget + int(level.get("budget_increase", 0))
    st.session_state.level_budget = (
        next_budget + int(level.get("bonus_budget", 0)) + st.session_state.performance_bonus
    )
    st.session_state.budget = st.session_state.level_budget
    st.session_state.hires_at_level_start = len(st.session_state.hired)
    st.session_state.assignments = {dept: "Select" for dept in DEPARTMENTS}
    st.session_state.last_assignments = dict(st.session_state.assignments)
    st.session_state.consultant_message = "GAMS Consultant is ready."
    st.session_state.last_city_health = st.session_state.city_health
    st.session_state.performance_bonus = 0
    st.session_state.current_crisis = level["crisis_name"]
    st.session_state.level_cleared = False
    st.session_state.recruitment_candidates_by_level[level_id] = list(level["candidates"])


def trait_team_effect(employee_name: str, team_size: int) -> int:
    """Simple teamwork effects for traits."""
    trait = EMPLOYEE_POOL[employee_name].get("hidden_trait", "")
    if not EMPLOYEE_POOL[employee_name].get("discovered"):
        return 0
    trait_effects = {
        "Lone Wolf": -8 if team_size > 1 else 4,
        "Catalyst": 8 if team_size > 1 else 2,
        "Needs Coffee": -6,
        "Precision Master": 6,
        "Fast Learner": 4,
        "Safety First": 4,
        "Night Owl": 3,
        "Optimizer": 5,
        "Energy Saver": 4,
        "Risk Scanner": 4,
        "Flow Tuner": 5,
        "Idea Spark": 4,
        "Data Sense": 4,
    }
    return trait_effects.get(trait, 0)


def eligible_for_department(employee_name: str, department: str) -> bool:
    """Department eligibility filter."""
    if department == DEPARTMENTS[0]:
        return int(EMPLOYEE_POOL[employee_name]["skill"]) >= 70
    return int(EMPLOYEE_POOL[employee_name]["analysis"]) >= 60


def department_base_score(employee_name: str, department: str) -> float:
    """Base score by department."""
    if department == DEPARTMENTS[0]:
        return float(EMPLOYEE_POOL[employee_name]["skill"])
    return float(EMPLOYEE_POOL[employee_name]["analysis"])


def update_city_health_on_hire(skill_value: int) -> None:
    """İşe alım sonrası şehir verimini küçük ölçekte artırır."""
    st.session_state.last_city_health = st.session_state.city_health
    delta = max(1.0, min(4.0, skill_value / 30))
    st.session_state.city_health = min(100.0, st.session_state.city_health + delta)


def average_teamwork(members: List[str]) -> float:
    """Average teamwork."""
    members = [m for m in members if m in EMPLOYEE_POOL]
    if not members:
        return 0.0
    return sum(float(EMPLOYEE_POOL[m]["teamwork"]) for m in members) / len(members)


def team_chemistry_scores(members: List[str]) -> Tuple[float, float, float]:
    """Rol çeşitliliği ve uyum skorları."""
    members = [m for m in members if m in EMPLOYEE_POOL]
    if not members:
        return 0.0, 0.0, 0.0
    unique_roles = len({EMPLOYEE_POOL[m]["role"] for m in members})
    role_diversity = min(100.0, unique_roles / len(members) * 100)
    teamwork_avg = average_teamwork(members)
    overall = min(100.0, role_diversity * 0.5 + teamwork_avg * 0.5)
    return role_diversity, teamwork_avg, overall


def build_root_cause(assignments: Dict[str, str]) -> List[str]:
    """Root cause list for crisis outcome."""
    reasons: List[str] = []
    if any(name == "Select" for name in assignments.values()):
        reasons.append("Assignments are incomplete.")
        return reasons

    dept_a, dept_b = DEPARTMENTS
    if not any(
        eligible_for_department(name, dept_a) for name in st.session_state.hired
    ):
        reasons.append("No eligible Technical profile for Department A.")
    if not any(
        eligible_for_department(name, dept_b) for name in st.session_state.hired
    ):
        reasons.append("No eligible Analytic profile for Department B.")

    for department, name in assignments.items():
        if name in EMPLOYEE_POOL and not eligible_for_department(name, department):
            reasons.append(f"{name} does not meet the requirement for {department}.")

    members = [name for name in assignments.values() if name in EMPLOYEE_POOL]
    if members:
        avg_teamwork = average_teamwork(members)
        if avg_teamwork < 70:
            reasons.append(
                f"Teamwork average {avg_teamwork:.0f} < 70 (synergy constraint)."
            )

    if not reasons:
        reasons.append("Expertise and synergy constraints passed; optimization gap remains.")
    return reasons

def assignment_score(assignments: Dict[str, str]) -> float:
    """Compute department-based team score."""
    members = [m for m in assignments.values() if m in EMPLOYEE_POOL]
    if not members:
        return 0.0
    if average_teamwork(members) < 70:
        return 0.0
    team_size = len(set(members))
    total = 0.0
    for department, name in assignments.items():
        if name in EMPLOYEE_POOL:
            total += department_base_score(name, department)
            total += trait_team_effect(name, team_size)
    return total




def render_sticky_top_bar(budget: int, efficiency: float) -> None:
    """Üstte sabit bütçe/verimlilik barı."""
    st.markdown(
        f"""
        <div class="sticky-bar">
            <div class="sticky-grid">
                <div class="sticky-item">
                    <div class="muted">Budget</div>
                    <strong>{budget} ₺</strong>
                </div>
                <div class="sticky-item">
                    <div class="muted">Current Efficiency</div>
                    <strong>{efficiency:.0f}%</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_top_metrics() -> None:
    """Üst metrikler: bütçe ve verimlilik."""
    efficiency = st.session_state.city_health
    delta = efficiency - st.session_state.last_city_health
    render_sticky_top_bar(st.session_state.budget, efficiency)
    col1, col2, col3 = st.columns([1.2, 1.2, 2.6])
    with col1:
        st.metric("Budget", f"{st.session_state.budget} ₺")
    with col2:
        st.metric("Current Efficiency", f"{efficiency:.0f}%", f"{delta:+.0f}%")
    with col3:
        st.progress(efficiency / 100, text="City Efficiency")


def render_consultant_box() -> None:
    """GAMS consultant box."""
    st.markdown(
        f"""
        <div class="consultant-box">
            <strong class="accent">🧠 GAMS Consultant</strong>
            <div class="muted" style="margin-top:6px;">{st.session_state.consultant_message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tech_structure() -> None:
    """Technical file structure table."""
    table = pd.DataFrame(
        [
            {
                "Dosya": "data.py",
                "İçerik": "Candidate salaries, skills (Technical, Analytic, Teamwork) and station requirements.",
            },
            {
                "Dosya": "solver.py",
                "İçerik": "GAMSPy code. Mathematical model with expertise and synergy constraints.",
            },
            {
                "Dosya": "app.py",
                "İçerik": "Streamlit UI. Where visuals and the GAMS engine meet.",
            },
        ]
    )
    st.table(table)


def render_person_card(
    name: str,
    context_key: str,
    show_action: bool = False,
    action_label: str = "İşe Al",
    action_disabled: bool = False,
) -> bool:
    """Flip kart görünümü."""
    info = EMPLOYEE_POOL[name]
    flip_key = f"flip_{context_key}_{name}"
    if flip_key not in st.session_state:
        st.session_state[flip_key] = False

    flip_state = st.session_state.get(flip_key, False)
    front_trait = info["hidden_trait"] if info["discovered"] else "Sırrı Bilinmiyor"
    back_trait = (
        info["trait_description"]
        if info["discovered"]
        else "Hidden trait not discovered yet."
    )
    skill_percent = int(info["skill"])
    analysis_percent = int(info["analysis"])
    teamwork_percent = int(info["teamwork"])

    card_html = f"""
    <div class="flip-card {'flipped' if flip_state else ''}">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <div class="avatar">{info['avatar']}</div>
                <h4>{name}</h4>
                <div class="muted">{info['role']}</div>
                <div><strong>Technical:</strong> {info['skill']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {skill_percent}%;"></div>
                </div>
                <div><strong>Analytic:</strong> {info['analysis']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {analysis_percent}%;"></div>
                </div>
                <div><strong>Teamwork:</strong> {info['teamwork']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {teamwork_percent}%;"></div>
                </div>
                <div><strong>Salary:</strong> {info['cost']} ₺</div>
                <div class="muted" style="margin-top:8px;">
                    <strong>Hidden Trait:</strong> {front_trait}
                </div>
            </div>
            <div class="flip-card-back">
                <div class="avatar">{info['avatar']}</div>
                <h4>{name} • Hidden Profile</h4>
                <div class="muted">{back_trait}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    st.toggle("Flip Card", key=flip_key)
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    if show_action:
        return st.button(action_label, key=f"{context_key}_action_{name}", disabled=action_disabled)
    return False


def render_recruitment(level: Dict[str, object]) -> None:
    """İK Aşaması."""
    level = LEVELS[st.session_state.level]
    st.markdown("## Recruitment Stage")
    st.write(level["description"])
    top_cols = st.columns([3, 1])
    with top_cols[1]:
        if st.button("🔄 Refresh Candidates", use_container_width=True):
            refresh_recruitment_candidates(st.session_state.level)
            st.rerun()
    question = level.get("question")
    if question:
        st.info(question)
    hire_count = int(level["hire_count"])
    hires_added = len(st.session_state.hired) - st.session_state.hires_at_level_start
    remaining_hires = max(0, hire_count - hires_added)
    st.info(
        f"New hires this level: **{hire_count}**. "
        f"Selected: **{hires_added}** / Remaining: **{remaining_hires}**"
    )

    candidate_names = get_recruitment_candidates(st.session_state.level)
    for row_start in range(0, len(candidate_names), 3):
        cols = st.columns(3)
        for col, name in zip(cols, candidate_names[row_start:row_start + 3]):
            info = EMPLOYEE_POOL[name]
            already_hired = name in st.session_state.hired
            limit_reached = hires_added >= hire_count

            with col:
                clicked = render_person_card(
                    name,
                    context_key="recruit",
                    show_action=True,
                    action_label="Add to Team",
                    action_disabled=already_hired or limit_reached,
                )
                if clicked:
                    if st.session_state.budget >= int(info["cost"]):
                        st.session_state.budget -= int(info["cost"])
                        st.session_state.hired.append(name)
                        update_city_health_on_hire(int(info["skill"]))
                        st.session_state.toast_message = f"{name} joined the team."
                        st.rerun()
                    else:
                        st.warning("Budget is insufficient. Pick a cheaper candidate.")

    st.markdown("## Current Team")
    if not st.session_state.hired:
        st.info("No team members yet.")
    else:
        for row_start in range(0, len(st.session_state.hired), 3):
            roster_cols = st.columns(3)
            for col, name in zip(roster_cols, st.session_state.hired[row_start:row_start + 3]):
                with col:
                    render_person_card(name, context_key="roster")

    if st.button("Lock Team and Start Crisis", type="primary"):
        if hires_added < hire_count:
            st.warning("You must use all new hires for this level before proceeding.")
        else:
            st.session_state.stage = "crisis"
            st.session_state.assignments = {dept: "Select" for dept in DEPARTMENTS}
            st.session_state.last_assignments = dict(st.session_state.assignments)
            st.rerun()


def build_trick_message(
    user_assignments: Dict[str, str],
    optimal_assignments: Dict[str, str],
) -> str:
    """Kısa ipucu üretir."""
    for department, optimal_name in optimal_assignments.items():
        user_name = user_assignments.get(department)
        if optimal_name != "Boş" and user_name != optimal_name:
            return (
                f"Trick: **{optimal_name}** fits best in **{department}**. "
                "Expertise filters favor this placement."
            )
    return "Trick: Minor improvements are still possible."


def update_consultant_message(assignments: Dict[str, str]) -> None:
    """Atama değiştiğinde GAMS ipucunu günceller."""
    if assignments == st.session_state.last_assignments:
        return

    st.session_state.consultant_message = "Analyzing..."
    if any(name == "Select" for name in assignments.values()):
        st.session_state.consultant_message = "Analyzing... complete the assignments."
        st.session_state.last_assignments = dict(assignments)
        return

    members = [name for name in assignments.values() if name in EMPLOYEE_POOL]
    if average_teamwork(members) < 70:
        st.session_state.consultant_message = (
            "Synergy Constraint: Teamwork average is below 70."
        )
        st.session_state.last_assignments = dict(assignments)
        return

    selected = {name: EMPLOYEE_POOL[name] for name in st.session_state.hired}
    gams_score, gams_assignments, feasible = get_gams_recommendation(
        selected, DEPARTMENTS
    )
    if not feasible:
        st.session_state.consultant_message = (
            "Engineering Deadlock: Expertise filters cannot be satisfied."
        )
        st.session_state.last_assignments = dict(assignments)
        return

    user_score = assignment_score(assignments)
    if user_score < gams_score:
        st.session_state.consultant_message = build_trick_message(
            assignments, gams_assignments
        )
    else:
        st.session_state.consultant_message = "Looks good. The gap is minimal."

    st.session_state.last_assignments = dict(assignments)


def render_crisis(level: Dict[str, object]) -> None:
    """Crisis stage."""
    level = LEVELS[st.session_state.level]
    st.markdown("## Daily Crisis")
    st.subheader(st.session_state.current_crisis)
    question = level.get("question")
    if question:
        st.info(question)
    st.caption("Select one eligible person per department, then start the day.")
    st.caption(
        "Assign specialists to departments. Department A requires Technical ≥ 70, "
        "Department B requires Analytic ≥ 60. Teamwork average must be ≥ 70."
    )
    st.caption("Tip: Balance technical and analytic strengths to avoid infeasible setups.")

    eligible_a_pool = any(
        eligible_for_department(name, DEPARTMENTS[0]) for name in st.session_state.hired
    )
    eligible_b_pool = any(
        eligible_for_department(name, DEPARTMENTS[1]) for name in st.session_state.hired
    )
    if not eligible_a_pool or not eligible_b_pool:
        st.error(
            "Engineering Deadlock: The team does not meet department requirements. "
            "No eligible profile for Production or R&D."
        )

    st.markdown("### Team Cards")
    for row_start in range(0, len(st.session_state.hired), 3):
        roster_cols = st.columns(3)
        for col, name in zip(roster_cols, st.session_state.hired[row_start:row_start + 3]):
            with col:
                render_person_card(name, context_key="crisis")

    st.markdown("### Department Assignments")
    cols = st.columns(2)
    assignments = dict(st.session_state.assignments)

    for col, department in zip(cols, DEPARTMENTS):
        used = {name for s, name in assignments.items() if s != department and name != "Select"}
        eligible = [
            name
            for name in st.session_state.hired
            if name not in used and eligible_for_department(name, department)
        ]
        options = ["Select"] + [
            name for name in eligible
        ]
        with col:
            selection = st.selectbox(
                department,
                options,
                index=options.index(assignments.get(department, "Select")),
                key=f"assign_{department}",
            )
        assignments[department] = selection

    st.session_state.assignments = assignments
    update_consultant_message(assignments)

    st.markdown("### Team Chemistry")
    members = [name for name in assignments.values() if name in EMPLOYEE_POOL]
    role_diversity, teamwork_avg, chemistry_overall = team_chemistry_scores(members)
    chem_cols = st.columns(3)
    chem_cols[0].metric("Role Diversity", f"{role_diversity:.0f}%")
    chem_cols[1].metric("Teamwork Avg", f"{teamwork_avg:.0f}%")
    chem_cols[2].metric("Overall Chemistry", f"{chemistry_overall:.0f}%")
    st.progress(chemistry_overall / 100, text="Team Chemistry")

    st.markdown("## Decision")
    if st.button("🔥 Start Day", type="primary"):
        if any(name == "Select" for name in assignments.values()):
            st.warning("Assign one person to each department.")
            return

        selected = {name: EMPLOYEE_POOL[name] for name in st.session_state.hired}
        gams_score, gams_assignments, feasible = get_gams_recommendation(
            selected, DEPARTMENTS
        )
        if not feasible:
            st.error("Engineering Deadlock: Expertise or synergy constraints failed.")
            st.markdown("### Root Cause Report")
            for reason in build_root_cause(assignments):
                st.warning(f"- {reason}")
            return

        user_score = assignment_score(assignments)
        efficiency_score = 0.0
        if gams_score > 0:
            efficiency_score = min(100.0, (user_score / gams_score) * 100)

        score_cols = st.columns(3)
        score_cols[0].metric("Your Score", f"{user_score:.0f}")
        score_cols[1].metric("GAMS Optimum", f"{gams_score:.0f}")
        score_cols[2].metric("Efficiency Score", f"{efficiency_score:.0f}%")
        st.progress(efficiency_score / 100, text="Efficiency Bar")
        st.caption("Threshold: 80% • Excellence: 90% (+500 ₺ bonus)")

        st.session_state.last_city_health = st.session_state.city_health
        if efficiency_score < 80:
            st.session_state.city_health = max(0.0, st.session_state.city_health - 5)
            reveal_name = next(
                (
                    name
                    for name in assignments.values()
                    if name in EMPLOYEE_POOL and not EMPLOYEE_POOL[name]["discovered"]
                ),
                None,
            )
            if reveal_name:
                discover_employee_trait(reveal_name)
                trait_desc = EMPLOYEE_POOL[reveal_name]["trait_description"]
                st.warning(
                    f"Discovery: {reveal_name}'s hidden trait revealed. {trait_desc}"
                )
            else:
                st.warning("GAMS Consultant: Below threshold, a better assignment exists.")
            st.markdown("### Root Cause Report")
            reasons = build_root_cause(assignments)
            reasons.append(f"Efficiency score {efficiency_score:.0f}% < 80 threshold.")
            for reason in reasons:
                st.warning(f"- {reason}")
        else:
            st.session_state.city_health = min(100.0, st.session_state.city_health + 15)
            st.success("Crisis resolved! You passed the threshold.")
            st.session_state.level_cleared = True
            current_day = len(st.session_state.crisis_history) + 1
            if (
                efficiency_score >= 90
                and st.session_state.level < max(LEVELS.keys())
                and st.session_state.last_bonus_awarded_day != current_day
            ):
                st.session_state.performance_bonus += 500
                st.session_state.last_bonus_awarded_day = current_day
                st.info("Excellence Bonus: +500 ₺ added to next level.")
            if st.session_state.level >= max(LEVELS.keys()):
                st.info("Congrats! All levels completed for now.")

        st.session_state.crisis_history.append(
            {
                "Day": len(st.session_state.crisis_history) + 1,
                "Your Score": user_score,
                "GAMS Optimum": gams_score,
                "Verimlilik (%)": efficiency_score,
                "City Efficiency": st.session_state.city_health,
            }
        )

    if st.session_state.crisis_history:
        st.markdown("### Crisis History (Last 3 Days)")
        history = st.session_state.crisis_history[-3:]
        df = pd.DataFrame(history).set_index("Day")
        df = df.rename(
            columns={
                "Verimlilik (%)": "Efficiency (%)",
            }
        )
        st.line_chart(df[["Your Score", "GAMS Optimum", "City Efficiency", "Efficiency (%)"]])

    if st.session_state.level_cleared and st.session_state.level < max(LEVELS.keys()):
        next_level = st.session_state.level + 1
        next_level_increase = int(LEVELS[next_level].get("budget_increase", 0))
        bonus = int(LEVELS[next_level].get("bonus_budget", 0)) + st.session_state.performance_bonus
        total_gain = next_level_increase + bonus
        if total_gain:
            st.info(f"Next level budget gain: +{total_gain} ₺")
        if st.button("➡️ Next Level", key="next_level_persist"):
            reset_level(next_level, carryover_budget=st.session_state.budget)
            # Force immediate rerender with the new level's question/crisis text.
            st.session_state.current_crisis = LEVELS[next_level]["crisis_name"]
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="The Factory Lab", layout="wide")
    apply_dashboard_theme()
    initialize_state()

    level = LEVELS[st.session_state.level]
    hire_count = int(level["hire_count"])
    hires_added = len(st.session_state.hired) - st.session_state.hires_at_level_start
    if st.session_state.stage == "crisis" and hires_added < hire_count:
        st.session_state.stage = "recruitment"
        level = LEVELS[st.session_state.level]
    if st.session_state.current_crisis != level["crisis_name"]:
        st.session_state.current_crisis = level["crisis_name"]

    st.title("The Factory Lab 🏭")
    st.caption("Build the team, handle the crisis, optimize the factory.")
    render_top_metrics()

    if st.session_state.toast_message:
        st.toast(st.session_state.toast_message, icon="✅")
        st.session_state.toast_message = ""

    main_cols = st.columns([3, 1])
    with main_cols[0]:
        if st.session_state.stage == "recruitment":
            render_recruitment(level)
        else:
            render_crisis(level)
    with main_cols[1]:
        render_consultant_box()
        with st.expander("Technical File Structure"):
            render_tech_structure()


if __name__ == "__main__":
    main()
