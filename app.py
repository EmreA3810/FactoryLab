"""Streamlit arayüzü: The Factory Lab 🏭."""

from __future__ import annotations

from typing import Dict, List, Tuple

import streamlit as st
import pandas as pd

from data import EMPLOYEE_POOL, LEVELS, discover_employee_trait

DEPARTMENTS = [
    "Departman A (Üretim & Mekanik)",
    "Departman B (Ar-Ge & Planlama)",
]
GAMS_BLUE = "#2f81f7"
SUCCESS_GREEN = "#3fb950"


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
            height: 260px;
            margin-bottom: 12px;
        }}
        .flip-card-inner {{
            position: relative;
            width: 100%;
            height: 260px;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }}
        .flip-card.flipped .flip-card-inner {{
            transform: rotateY(180deg);
        }}
        .flip-card-front, .flip-card-back {{
            position: absolute;
            width: 100%;
            height: 260px;
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
        level = LEVELS[st.session_state.level]
        st.session_state.level_budget = level["budget"] + level.get("bonus_budget", 0)
    if "budget" not in st.session_state:
        st.session_state.budget = st.session_state.level_budget
    if "hired" not in st.session_state:
        st.session_state.hired = []
    if "hires_at_level_start" not in st.session_state:
        st.session_state.hires_at_level_start = len(st.session_state.hired)
    if "assignments" not in st.session_state:
        st.session_state.assignments = {dept: "Seçiniz" for dept in DEPARTMENTS}
    if "consultant_message" not in st.session_state:
        st.session_state.consultant_message = "GAMS Danışmanı hazır."
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


def reset_level(level_id: int) -> None:
    """Yeni seviyeye geçişte state resetler."""
    level = LEVELS[level_id]
    st.session_state.level = level_id
    st.session_state.stage = "recruitment"
    st.session_state.level_budget = (
        level["budget"] + level.get("bonus_budget", 0) + st.session_state.performance_bonus
    )
    st.session_state.budget = st.session_state.level_budget
    st.session_state.hires_at_level_start = len(st.session_state.hired)
    st.session_state.assignments = {dept: "Seçiniz" for dept in DEPARTMENTS}
    st.session_state.last_assignments = dict(st.session_state.assignments)
    st.session_state.consultant_message = "GAMS Danışmanı hazır."
    st.session_state.last_city_health = st.session_state.city_health
    st.session_state.performance_bonus = 0


def trait_team_effect(employee_name: str, team_size: int) -> int:
    """Takım çalışması için basit trait etkileri."""
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
    """Departman uzmanlık filtresi."""
    if department == DEPARTMENTS[0]:
        return int(EMPLOYEE_POOL[employee_name]["skill"]) >= 70
    return int(EMPLOYEE_POOL[employee_name]["analysis"]) >= 60


def department_base_score(employee_name: str, department: str) -> float:
    """Departmana göre temel puan."""
    if department == DEPARTMENTS[0]:
        return float(EMPLOYEE_POOL[employee_name]["skill"])
    return float(EMPLOYEE_POOL[employee_name]["analysis"])


def update_city_health_on_hire(skill_value: int) -> None:
    """İşe alım sonrası şehir verimini küçük ölçekte artırır."""
    st.session_state.last_city_health = st.session_state.city_health
    delta = max(1.0, min(4.0, skill_value / 30))
    st.session_state.city_health = min(100.0, st.session_state.city_health + delta)


def average_teamwork(members: List[str]) -> float:
    """Takım çalışması ortalaması."""
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
    """Kriz sonucu için kök neden listesi."""
    reasons: List[str] = []
    if any(name == "Seçiniz" for name in assignments.values()):
        reasons.append("Atamalar tamamlanmadı.")
        return reasons

    dept_a, dept_b = DEPARTMENTS
    if not any(
        eligible_for_department(name, dept_a) for name in st.session_state.hired
    ):
        reasons.append("Departman A için uygun teknik puanlı aday yok.")
    if not any(
        eligible_for_department(name, dept_b) for name in st.session_state.hired
    ):
        reasons.append("Departman B için uygun analiz puanlı aday yok.")

    for department, name in assignments.items():
        if name in EMPLOYEE_POOL and not eligible_for_department(name, department):
            reasons.append(f"{name}, {department} uzmanlık şartını karşılamıyor.")

    members = [name for name in assignments.values() if name in EMPLOYEE_POOL]
    if members:
        avg_teamwork = average_teamwork(members)
        if avg_teamwork < 70:
            reasons.append(
                f"Takım çalışması ortalaması {avg_teamwork:.0f} < 70 (sinerji kısıtı)."
            )

    if not reasons:
        reasons.append("Uzmanlık ve sinerji kısıtları sağlandı, optimizasyon farkı kaldı.")
    return reasons

def assignment_score(assignments: Dict[str, str]) -> float:
    """Departman bazlı takım verimini hesaplar."""
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


def get_gams_recommendation(
    assigned_employees: Dict[str, str],
    departments: List[str],
) -> Tuple[float, Dict[str, str], bool]:
    """Mock GAMS danışmanı - gerçek solver daha sonra eklenecek."""
    employees = st.session_state.hired
    best_score = -1.0
    best_assignments = {dept: "Boş" for dept in departments}

    dept_a, dept_b = departments
    eligible_a = [e for e in employees if eligible_for_department(e, dept_a)]
    eligible_b = [e for e in employees if eligible_for_department(e, dept_b)]

    if not eligible_a or not eligible_b:
        return 0.0, best_assignments, False

    for emp_a in eligible_a:
        for emp_b in eligible_b:
            if emp_a == emp_b:
                continue
            if average_teamwork([emp_a, emp_b]) < 70:
                continue
            candidate = {dept_a: emp_a, dept_b: emp_b}
            score = assignment_score(candidate)
            if score > best_score:
                best_score = score
                best_assignments = dict(candidate)

    if best_score < 0:
        return 0.0, best_assignments, False
    return max(best_score, 0.0), best_assignments, True


def render_sticky_top_bar(budget: int, efficiency: float) -> None:
    """Üstte sabit bütçe/verimlilik barı."""
    st.markdown(
        f"""
        <div class="sticky-bar">
            <div class="sticky-grid">
                <div class="sticky-item">
                    <div class="muted">Bütçe</div>
                    <strong>{budget} ₺</strong>
                </div>
                <div class="sticky-item">
                    <div class="muted">Mevcut Verimlilik</div>
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
        st.metric("Bütçe", f"{st.session_state.budget} ₺")
    with col2:
        st.metric("Mevcut Verimlilik", f"{efficiency:.0f}%", f"{delta:+.0f}%")
    with col3:
        st.progress(efficiency / 100, text="Şehir Verimliliği")


def render_consultant_box() -> None:
    """GAMS Danışmanı kutusu."""
    st.markdown(
        f"""
        <div class="consultant-box">
            <strong class="accent">🧠 GAMS Danışmanı</strong>
            <div class="muted" style="margin-top:6px;">{st.session_state.consultant_message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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

    with st.container():
        flip_state = st.toggle("Kartı Çevir", key=flip_key)
    front_trait = info["hidden_trait"] if info["discovered"] else "Sırrı Bilinmiyor"
    back_trait = (
        info["trait_description"]
        if info["discovered"]
        else "Gizli özellik henüz keşfedilmedi."
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
                <div><strong>Teknik:</strong> {info['skill']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {skill_percent}%;"></div>
                </div>
                <div><strong>Analiz:</strong> {info['analysis']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {analysis_percent}%;"></div>
                </div>
                <div><strong>Takım Çalışması:</strong> {info['teamwork']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {teamwork_percent}%;"></div>
                </div>
                <div><strong>Maaş:</strong> {info['cost']} ₺</div>
                <div class="muted" style="margin-top:8px;">
                    <strong>Gizli Özellik:</strong> {front_trait}
                </div>
            </div>
            <div class="flip-card-back">
                <div class="avatar">{info['avatar']}</div>
                <h4>{name} • Gizli Profil</h4>
                <div class="muted">{back_trait}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    if show_action:
        return st.button(action_label, key=f"{context_key}_action_{name}", disabled=action_disabled)
    return False


def render_recruitment(level: Dict[str, object]) -> None:
    """İK Aşaması."""
    st.markdown("## İK Aşaması (Recruitment)")
    st.write(level["description"])
    hire_count = int(level["hire_count"])
    hires_added = len(st.session_state.hired) - st.session_state.hires_at_level_start
    remaining_hires = max(0, hire_count - hires_added)
    st.info(
        f"Bu seviyede yeni alım hakkı: **{hire_count}** kişi. "
        f"Seçilen: **{hires_added}** / Kalan: **{remaining_hires}**"
    )

    candidate_names = level["candidates"]
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
                    action_label="Ekibe Kat",
                    action_disabled=already_hired or limit_reached,
                )
                if clicked:
                    if st.session_state.budget >= int(info["cost"]):
                        st.session_state.budget -= int(info["cost"])
                        st.session_state.hired.append(name)
                        update_city_health_on_hire(int(info["skill"]))
                        st.session_state.toast_message = f"{name} ekibe katıldı."
                        st.rerun()
                    else:
                        st.warning("Bütçe yetersiz. Daha uygun bir aday seçmelisin.")

    st.markdown("## Ekibe Katılanlar")
    if not st.session_state.hired:
        st.info("Henüz ekip oluşturulmadı.")
    else:
        for row_start in range(0, len(st.session_state.hired), 3):
            roster_cols = st.columns(3)
            for col, name in zip(roster_cols, st.session_state.hired[row_start:row_start + 3]):
                with col:
                    render_person_card(name, context_key="roster")

    if st.button("Ekibi Kilitle ve Krize Geç", type="primary"):
        if hires_added < hire_count:
            st.warning("Krize geçmek için bu seviyedeki alım hakkını doldurmalısın.")
        else:
            st.session_state.stage = "crisis"
            st.session_state.assignments = {dept: "Seçiniz" for dept in DEPARTMENTS}
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
                f"Trick: **{optimal_name}** için en uygun yer **{department}** görünüyor. "
                "Uzmanlık filtresi burada daha güçlü çalışıyor."
            )
    return "Trick: Atamanın küçük iyileştirmelere ihtiyacı var."


def update_consultant_message(assignments: Dict[str, str]) -> None:
    """Atama değiştiğinde GAMS ipucunu günceller."""
    if assignments == st.session_state.last_assignments:
        return

    st.session_state.consultant_message = "Analiz ediliyor..."
    if any(name == "Seçiniz" for name in assignments.values()):
        st.session_state.consultant_message = "Analiz ediliyor... Atamayı tamamla."
        st.session_state.last_assignments = dict(assignments)
        return

    members = [name for name in assignments.values() if name in EMPLOYEE_POOL]
    if average_teamwork(members) < 70:
        st.session_state.consultant_message = (
            "Sinerji Kısıtı: Takım çalışması ortalaması 70'in altında."
        )
        st.session_state.last_assignments = dict(assignments)
        return

    gams_score, gams_assignments, feasible = get_gams_recommendation(
        assignments, DEPARTMENTS
    )
    if not feasible:
        st.session_state.consultant_message = (
            "Mühendislik Çıkmazı: Uzmanlık filtreleri sağlanamıyor."
        )
        st.session_state.last_assignments = dict(assignments)
        return

    user_score = assignment_score(assignments)
    if user_score < gams_score:
        st.session_state.consultant_message = build_trick_message(
            assignments, gams_assignments
        )
    else:
        st.session_state.consultant_message = "İyi gidiyorsun. Fark oldukça düşük."

    st.session_state.last_assignments = dict(assignments)


def render_crisis(level: Dict[str, object]) -> None:
    """Kriz aşaması."""
    st.markdown("## Daily Crisis (The Challenge)")
    st.subheader(level["crisis_name"])
    st.caption(
        "Uzmanlık filtreleri: Departman A için Teknik ≥ 70, "
        "Departman B için Analiz ≥ 60."
    )

    eligible_a_pool = any(
        eligible_for_department(name, DEPARTMENTS[0]) for name in st.session_state.hired
    )
    eligible_b_pool = any(
        eligible_for_department(name, DEPARTMENTS[1]) for name in st.session_state.hired
    )
    if not eligible_a_pool or not eligible_b_pool:
        st.error(
            "Mühendislik Çıkmazı: Ekip, departman uzmanlıklarına uymuyor. "
            "Ar-Ge veya Üretim için uygun profil yok."
        )

    st.markdown("### Ekip Kartları")
    for row_start in range(0, len(st.session_state.hired), 3):
        roster_cols = st.columns(3)
        for col, name in zip(roster_cols, st.session_state.hired[row_start:row_start + 3]):
            with col:
                render_person_card(name, context_key="crisis")

    st.markdown("### Departman Atamaları")
    cols = st.columns(2)
    assignments = dict(st.session_state.assignments)

    for col, department in zip(cols, DEPARTMENTS):
        used = {name for s, name in assignments.items() if s != department and name != "Seçiniz"}
        eligible = [
            name
            for name in st.session_state.hired
            if name not in used and eligible_for_department(name, department)
        ]
        options = ["Seçiniz"] + [
            name for name in eligible
        ]
        with col:
            selection = st.selectbox(
                department,
                options,
                index=options.index(assignments.get(department, "Seçiniz")),
                key=f"assign_{department}",
            )
        assignments[department] = selection

    st.session_state.assignments = assignments
    update_consultant_message(assignments)

    st.markdown("### Takım Kimyası")
    members = [name for name in assignments.values() if name in EMPLOYEE_POOL]
    role_diversity, teamwork_avg, chemistry_overall = team_chemistry_scores(members)
    chem_cols = st.columns(3)
    chem_cols[0].metric("Rol Çeşitliliği", f"{role_diversity:.0f}%")
    chem_cols[1].metric("Uyum Skoru", f"{teamwork_avg:.0f}%")
    chem_cols[2].metric("Genel Kimya", f"{chemistry_overall:.0f}%")
    st.progress(chemistry_overall / 100, text="Takım Kimyası")

    st.markdown("## Günün Kararı")
    if st.button("🔥 Günü Başlat", type="primary"):
        if any(name == "Seçiniz" for name in assignments.values()):
            st.warning("Lütfen her iki departmana da bir personel ata.")
            return

        gams_score, gams_assignments, feasible = get_gams_recommendation(
            assignments, DEPARTMENTS
        )
        if not feasible:
            st.error("Mühendislik Çıkmazı: Uzmanlık veya sinerji kısıtı sağlanamadı.")
            st.markdown("### Kök Neden Raporu")
            for reason in build_root_cause(assignments):
                st.warning(f"- {reason}")
            return

        user_score = assignment_score(assignments)
        efficiency_score = 0.0
        if gams_score > 0:
            efficiency_score = min(100.0, (user_score / gams_score) * 100)

        score_cols = st.columns(3)
        score_cols[0].metric("Senin Skorun", f"{user_score:.0f}")
        score_cols[1].metric("GAMS Optimum", f"{gams_score:.0f}")
        score_cols[2].metric("Verimlilik Skoru", f"{efficiency_score:.0f}%")
        st.progress(efficiency_score / 100, text="Verimlilik Barı")
        st.caption("Baraj: %80 • Mükemmellik: %90 (+500 ₺ bonus)")

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
                    f"Keşif: {reveal_name} için gizli özellik açıldı. {trait_desc}"
                )
            else:
                st.warning("GAMS Danışmanı: Baraj altında kaldın, daha iyi bir atama mümkün.")
            st.markdown("### Kök Neden Raporu")
            reasons = build_root_cause(assignments)
            reasons.append(f"Verimlilik skoru {efficiency_score:.0f}% < 80 barajı.")
            for reason in reasons:
                st.warning(f"- {reason}")
        else:
            st.session_state.city_health = min(100.0, st.session_state.city_health + 15)
            st.success("Kriz başarıyla yönetildi! Barajı geçtin.")
            current_day = len(st.session_state.crisis_history) + 1
            if (
                efficiency_score >= 90
                and st.session_state.level < max(LEVELS.keys())
                and st.session_state.last_bonus_awarded_day != current_day
            ):
                st.session_state.performance_bonus += 500
                st.session_state.last_bonus_awarded_day = current_day
                st.info("Mükemmellik Bonus'u: Sonraki seviye için +500 ₺ kazandın.")
            if st.session_state.level < max(LEVELS.keys()):
                next_level = st.session_state.level + 1
                bonus = LEVELS[next_level].get("bonus_budget", 0) + st.session_state.performance_bonus
                if bonus:
                    st.info(f"Yeni seviyede ek bütçe: +{bonus} ₺")
                if st.button("➡️ Sonraki Seviye"):
                    reset_level(next_level)
                    st.rerun()
            else:
                st.info("Tebrikler! Şimdilik tüm seviyeler tamamlandı.")

        st.session_state.crisis_history.append(
            {
                "Gün": len(st.session_state.crisis_history) + 1,
                "Senin Skorun": user_score,
                "GAMS Optimum": gams_score,
                "Verimlilik (%)": efficiency_score,
                "Şehir Verimliliği": st.session_state.city_health,
            }
        )

    if st.session_state.crisis_history:
        st.markdown("### Kriz Tarihçesi (Son 3 Gün)")
        history = st.session_state.crisis_history[-3:]
        df = pd.DataFrame(history).set_index("Gün")
        st.line_chart(df[["Senin Skorun", "GAMS Optimum", "Şehir Verimliliği", "Verimlilik (%)"]])


def main() -> None:
    st.set_page_config(page_title="The Factory Lab", layout="wide")
    apply_dashboard_theme()
    initialize_state()

    level = LEVELS[st.session_state.level]

    st.title("The Factory Lab 🏭")
    st.caption("Ekip kur, krizi yönet, fabrikayı optimize et.")
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


if __name__ == "__main__":
    main()
