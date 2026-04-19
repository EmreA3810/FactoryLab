# The Factory Lab 🏭

A cyberpunk-themed Streamlit management game where you recruit engineers, manage budget, and solve daily factory crises with optimization support from **GAMSPy**.

## What this project does

- Multi-level recruitment + crisis gameplay loop
- Budget progression between levels (`+2000`, `+3000`, and performance bonus)
- Candidate cards with stats, hidden traits, and role-based avatars
- Random candidate refresh during recruitment
- GAMS-backed assignment recommendation with constraints:
  - Department A: Technical ≥ 70
  - Department B: Analytic ≥ 60
  - Teamwork average ≥ 70
- Cyberpunk dashboard UI with configurable background image

## Tech stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [GAMSPy](https://gamspy.readthedocs.io/)

## Project structure

```text
FactoryLab/
├─ app.py               # Streamlit UI, game flow, theme, session state
├─ data.py              # Candidate pool and level definitions
├─ solver.py            # GAMSPy optimization model
└─ assets/
   └─ factory_background.png
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install streamlit pandas gamspy
```

> If GAMSPy requires a local GAMS setup in your environment, complete that setup first.

## Run the app

```bash
streamlit run app.py
```

## Gameplay flow

1. **Recruitment Stage**: Hire the required number of candidates for the current level.
2. **Crisis Stage**: Assign team members to departments and start the day.
3. **Scoring**:
   - `< 80%` efficiency: fail threshold
   - `≥ 80%` efficiency: level clear
   - `≥ 90%` efficiency: extra bonus for next level
4. Move to next level and continue.

## Customization

- **Background image**: replace `assets/factory_background.png`
- **Candidates/levels**: edit `data.py`
- **Theme/UI behavior**: edit `apply_dashboard_theme()` in `app.py`
- **Optimization logic**: edit `get_gams_recommendation()` in `solver.py`

