"""Streamlit arayüzü: The Factory Lab 🏭."""

from __future__ import annotations

from typing import Dict, List, Tuple

import streamlit as st

from data import EMPLOYEE_POOL, LEVELS, discover_employee_trait

TEAM_SLOTS = ["Ekip Üyesi 1", "Ekip Üyesi 2"]
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
    if "assignments" not in st.session_state:
        st.session_state.assignments = {slot: "Seçiniz" for slot in TEAM_SLOTS}
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


def reset_level(level_id: int) -> None:
    """Yeni seviyeye geçişte state resetler."""
    level = LEVELS[level_id]
    st.session_state.level = level_id
    st.session_state.stage = "recruitment"
    st.session_state.level_budget = level["budget"] + level.get("bonus_budget", 0)
    st.session_state.budget = st.session_state.level_budget
    st.session_state.hired = []
    st.session_state.assignments = {slot: "Seçiniz" for slot in TEAM_SLOTS}
    st.session_state.last_assignments = dict(st.session_state.assignments)
    st.session_state.consultant_message = "GAMS Danışmanı hazır."
    st.session_state.last_city_health = st.session_state.city_health


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
    }
    return trait_effects.get(trait, 0)


def get_team_limit(level_id: int, level_budget: int) -> int:
    """Bütçeye ve seviyeye göre işe alım limiti."""
    base_limit = 4 if level_budget >= 9000 else 3
    return base_limit + max(0, level_id - 1) * 2


def update_city_health_on_hire(skill_value: int) -> None:
    """İşe alım sonrası şehir verimini küçük ölçekte artırır."""
    st.session_state.last_city_health = st.session_state.city_health
    delta = max(1.0, min(4.0, skill_value / 30))
    st.session_state.city_health = min(100.0, st.session_state.city_health + delta)


def team_score(members: List[str]) -> float:
    """Takım verimini hesaplar."""
    members = [m for m in members if m in EMPLOYEE_POOL]
    if not members:
        return 0.0
    base = sum(float(EMPLOYEE_POOL[m]["skill"]) for m in members)
    synergy = 0
    if len(members) == 2:
        roles = {EMPLOYEE_POOL[m]["role"] for m in members}
        if len(roles) > 1:
            synergy += 6
    for m in members:
        synergy += trait_team_effect(m, len(members))
    return base + synergy


def get_gams_recommendation(
    assigned_employees: Dict[str, str],
    slots: List[str],
) -> Tuple[float, Dict[str, str]]:
    """Mock GAMS danışmanı - gerçek solver daha sonra eklenecek."""
    employees = st.session_state.hired
    best_score = -1.0
    best_team: List[str] = []

    for i, emp in enumerate(employees):
        score_single = team_score([emp])
        if score_single > best_score:
            best_score = score_single
            best_team = [emp]
        for j in range(i + 1, len(employees)):
            team = [emp, employees[j]]
            score_pair = team_score(team)
            if score_pair > best_score:
                best_score = score_pair
                best_team = team

    assignments = {slot: "Boş" for slot in slots}
    for idx, member in enumerate(best_team):
        if idx < len(slots):
            assignments[slots[idx]] = member
    return max(best_score, 0.0), assignments


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

    card_html = f"""
    <div class="flip-card {'flipped' if flip_state else ''}">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <div class="avatar">{info['avatar']}</div>
                <h4>{name}</h4>
                <div class="muted">{info['role']}</div>
                <div><strong>Hard Skill:</strong> {info['skill']}/100</div>
                <div class="progress" style="margin:6px 0;">
                    <div class="progress-bar" style="width: {skill_percent}%;"></div>
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
    team_limit = get_team_limit(st.session_state.level, st.session_state.level_budget)
    st.info(
        f"Ekip limiti: **{team_limit}** kişi. "
        f"Seçilen: **{len(st.session_state.hired)}**"
    )

    candidate_names = level["candidates"]
    for row_start in range(0, len(candidate_names), 3):
        cols = st.columns(3)
        for col, name in zip(cols, candidate_names[row_start:row_start + 3]):
            info = EMPLOYEE_POOL[name]
            already_hired = name in st.session_state.hired
            limit_reached = len(st.session_state.hired) >= team_limit

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
        if len(st.session_state.hired) < 1:
            st.warning("Krize geçmek için en az bir kişi seçmelisin.")
        else:
            st.session_state.stage = "crisis"
            st.session_state.assignments = {slot: "Seçiniz" for slot in TEAM_SLOTS}
            st.session_state.last_assignments = dict(st.session_state.assignments)
            st.rerun()


def build_trick_message(
    user_members: List[str],
    optimal_members: List[str],
) -> str:
    """Kısa ipucu üretir."""
    user_set = {m for m in user_members if m}
    optimal_set = {m for m in optimal_members if m}
    if optimal_set and optimal_set != user_set:
        if len(optimal_set) == 2:
            a, b = list(optimal_set)
            return (
                f"Trick: **{a}** ile **{b}** birlikte çalışırsa verim artabilir. "
                "Bu ikilinin uyumu daha yüksek görünüyor."
            )
        if len(optimal_set) == 1:
            sole = next(iter(optimal_set))
            return (
                f"Trick: **{sole}** bu krizi tek başına daha temiz çözebilir."
            )
    return "Trick: Atamanın küçük iyileştirmelere ihtiyacı var."


def update_consultant_message(assignments: Dict[str, str]) -> None:
    """Atama değiştiğinde GAMS ipucunu günceller."""
    if assignments == st.session_state.last_assignments:
        return

    st.session_state.consultant_message = "Analiz ediliyor..."
    members = [name for name in assignments.values() if name != "Seçiniz"]
    if not members:
        st.session_state.consultant_message = "Analiz ediliyor... Ekibini seç."
        st.session_state.last_assignments = dict(assignments)
        return

    gams_score, gams_assignments = get_gams_recommendation(assignments, TEAM_SLOTS)
    user_score = team_score(members)
    optimal_members = [name for name in gams_assignments.values() if name != "Boş"]
    if user_score < gams_score:
        st.session_state.consultant_message = build_trick_message(
            members, optimal_members
        )
    else:
        st.session_state.consultant_message = "İyi gidiyorsun. Fark oldukça düşük."

    st.session_state.last_assignments = dict(assignments)


def render_crisis(level: Dict[str, object]) -> None:
    """Kriz aşaması."""
    st.markdown("## Daily Crisis (The Challenge)")
    st.subheader(level["crisis_name"])

    st.markdown("### Ekip Kartları")
    for row_start in range(0, len(st.session_state.hired), 3):
        roster_cols = st.columns(3)
        for col, name in zip(roster_cols, st.session_state.hired[row_start:row_start + 3]):
            with col:
                render_person_card(name, context_key="crisis")

    st.markdown("### Birlikte Çalışma Ekibi")
    cols = st.columns(2)
    assignments = dict(st.session_state.assignments)

    for col, slot in zip(cols, TEAM_SLOTS):
        used = {name for s, name in assignments.items() if s != slot and name != "Seçiniz"}
        options = ["Seçiniz"] + [
            name for name in st.session_state.hired if name not in used
        ]
        with col:
            selection = st.selectbox(
                slot,
                options,
                index=options.index(assignments.get(slot, "Seçiniz")),
                key=f"assign_{slot}",
            )
        assignments[slot] = selection

    st.session_state.assignments = assignments
    update_consultant_message(assignments)

    st.markdown("## Günün Kararı")
    if st.button("🔥 Günü Başlat", type="primary"):
        members = [name for name in assignments.values() if name != "Seçiniz"]
        if not members:
            st.warning("Lütfen en az bir ekip üyesi seç.")
            return

        user_score = team_score(members)
        gams_score, gams_assignments = get_gams_recommendation(assignments, TEAM_SLOTS)

        score_cols = st.columns(2)
        score_cols[0].metric("Senin Skorun", f"{user_score:.0f}")
        score_cols[1].metric("GAMS Optimum", f"{gams_score:.0f}")

        st.session_state.last_city_health = st.session_state.city_health
        if user_score < gams_score:
            st.session_state.city_health = max(0.0, st.session_state.city_health - 5)
            reveal_name = next(
                (
                    name
                    for name in members
                    if name in EMPLOYEE_POOL and not EMPLOYEE_POOL[name]["discovered"]
                ),
                None,
            )
            if reveal_name:
                discover_employee_trait(reveal_name)
                st.warning(
                    f"GAMS Danışmanı: Daha iyi bir atama mümkün. "
                    f"{reveal_name} için gizli ipucu açıldı."
                )
            else:
                st.warning("GAMS Danışmanı: Daha iyi bir atama mümkün.")
        else:
            st.session_state.city_health = min(100.0, st.session_state.city_health + 15)
            st.success("Kriz başarıyla yönetildi! Yeni seviye açıldı.")
            if st.session_state.level < max(LEVELS.keys()):
                next_level = st.session_state.level + 1
                bonus = LEVELS[next_level].get("bonus_budget", 0)
                if bonus:
                    st.info(f"Yeni seviyede ek bütçe: +{bonus} ₺")
                if st.button("➡️ Sonraki Seviye"):
                    reset_level(next_level)
                    st.rerun()
            else:
                st.info("Tebrikler! Şimdilik tüm seviyeler tamamlandı.")


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
