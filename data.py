"""Oyun durumu ve sabit veri sözlükleri."""

from __future__ import annotations

from typing import Any, Dict

# 1. İK Aday Havuzu (Personel Kartları)
EMPLOYEE_POOL: Dict[str, Dict[str, Any]] = {
    "Arda": {
        "role": "Makine Operatörü",
        "skill": 85,
        "analysis": 42,
        "teamwork": 55,
        "cost": 1300,
        "avatar": "🛠️",
        "hidden_trait": "Lone Wolf",
        "trait_description": (
            "Lone Wolf: Arda yalnız çalışmayı sever. Diğer istasyonda biri varsa stres yapar "
            "(Negatif etki)."
        ),
        "discovered": False,
    },
    "Merve": {
        "role": "Kalite Kontrol",
        "skill": 90,
        "analysis": 72,
        "teamwork": 80,
        "cost": 1600,
        "avatar": "🔬",
        "hidden_trait": "Catalyst",
        "trait_description": (
            "Catalyst: Merve harika bir sinerji yaratır. Girdiği istasyonun verimini artırır "
            "(Pozitif etki)."
        ),
        "discovered": False,
    },
    "Can": {
        "role": "Lojistik Uzmanı",
        "skill": 75,
        "analysis": 55,
        "teamwork": 62,
        "cost": 900,
        "avatar": "🚚",
        "hidden_trait": "Needs Coffee",
        "trait_description": (
            "Needs Coffee: Can bugün kahve içmedi, temel verimi GAMS modelinde 10 puan düşük "
            "hesaplanacak."
        ),
        "discovered": False,
    },
    "Mina": {
        "role": "Proses Mühendisi",
        "skill": 95,
        "analysis": 82,
        "teamwork": 78,
        "cost": 1800,
        "avatar": "🧪",
        "hidden_trait": "Precision Master",
        "trait_description": (
            "Precision Master: Mina hassas işlerde hatayı %20 azaltır (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Emre": {
        "role": "Hat Lideri",
        "skill": 80,
        "analysis": 60,
        "teamwork": 70,
        "cost": 1200,
        "avatar": "📈",
        "hidden_trait": "Fast Learner",
        "trait_description": (
            "Fast Learner: Emre yeni görevlerde hızla uyum sağlar (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Selin": {
        "role": "Bakım Uzmanı",
        "skill": 78,
        "analysis": 48,
        "teamwork": 74,
        "cost": 1000,
        "avatar": "🧰",
        "hidden_trait": "Safety First",
        "trait_description": (
            "Safety First: Selin riskleri azaltır, hat güvenliğini yükseltir (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Bora": {
        "role": "Vardiya Koordinatörü",
        "skill": 88,
        "analysis": 66,
        "teamwork": 72,
        "cost": 1700,
        "avatar": "🧭",
        "hidden_trait": "Night Owl",
        "trait_description": (
            "Night Owl: Bora düşük tempolu anlarda bile verimi korur (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Zeynep": {
        "role": "Planlama Analisti",
        "skill": 82,
        "analysis": 78,
        "teamwork": 76,
        "cost": 1300,
        "avatar": "📊",
        "hidden_trait": "Optimizer",
        "trait_description": (
            "Optimizer: Zeynep akışı yeniden düzenleyip darboğazı azaltır (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Kerem": {
        "role": "Enerji Mühendisi",
        "skill": 86,
        "analysis": 58,
        "teamwork": 68,
        "cost": 1600,
        "avatar": "⚡",
        "hidden_trait": "Energy Saver",
        "trait_description": (
            "Energy Saver: Kerem enerji kaybını azaltır, süreçleri dengeler (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Ece": {
        "role": "Risk Analisti",
        "skill": 84,
        "analysis": 74,
        "teamwork": 73,
        "cost": 1100,
        "avatar": "🛰️",
        "hidden_trait": "Risk Scanner",
        "trait_description": (
            "Risk Scanner: Ece riskli noktaları hızla tespit eder (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Onur": {
        "role": "Süreç Tasarımcısı",
        "skill": 89,
        "analysis": 68,
        "teamwork": 71,
        "cost": 1200,
        "avatar": "🧩",
        "hidden_trait": "Flow Tuner",
        "trait_description": (
            "Flow Tuner: Onur akışı sadeleştirip darboğazı azaltır (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Ayşe": {
        "role": "İnovasyon Mühendisi",
        "skill": 83,
        "analysis": 76,
        "teamwork": 82,
        "cost": 1400,
        "avatar": "💡",
        "hidden_trait": "Idea Spark",
        "trait_description": (
            "Idea Spark: Ayşe yeni fikirlerle çözüm üretimini hızlandırır (Pozitif etki)."
        ),
        "discovered": False,
    },
    "Deniz": {
        "role": "Veri Uzmanı",
        "skill": 77,
        "analysis": 70,
        "teamwork": 79,
        "cost": 1350,
        "avatar": "🧠",
        "hidden_trait": "Data Sense",
        "trait_description": (
            "Data Sense: Deniz veriye dayalı kararları güçlendirir (Pozitif etki)."
        ),
        "discovered": False,
    },
}

# 2. Level ve Kriz Verileri
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Level 1: Peak Hour Chaos",
        "crisis_name": "Üretim Hattında Darboğaz!",
        "description": "6 aday arasından 4 kişilik ekip kur. Bütçeyi dikkatli kullan.",
        "stations": ["İstasyon 1", "İstasyon 2"],
        "budget": 5000,
        "bonus_budget": 0,
        "candidates": ["Arda", "Merve", "Can", "Selin", "Emre", "Zeynep"],
        "hire_count": 4,
        "progress_target": 0.35,
    },
    2: {
        "name": "Level 2: Expansion Shift",
        "crisis_name": "Kalite Sapması Alarmı!",
        "description": "3 aday arasından 1 kişi seç. Ekibin dengesini bozma.",
        "stations": ["İstasyon 1", "İstasyon 2"],
        "budget": 7500,
        "bonus_budget": 1000,
        "candidates": ["Mina", "Bora", "Ece"],
        "hire_count": 1,
        "progress_target": 0.7,
    },
    3: {
        "name": "Level 3: Full Scale Rush",
        "crisis_name": "Tedarik Zinciri Kilitlenmesi!",
        "description": "4 aday arasından 2 kişi seç. Yüksek analiz puanı kritik.",
        "stations": ["İstasyon 1", "İstasyon 2"],
        "budget": 11000,
        "bonus_budget": 1500,
        "candidates": ["Kerem", "Onur", "Ayşe", "Deniz"],
        "hire_count": 2,
        "progress_target": 0.95,
    },
}


def discover_employee_trait(employee_name: str) -> bool:
    """Bir personelin gizli özelliğini 'keşfedildi' olarak işaretler."""
    if employee_name in EMPLOYEE_POOL:
        EMPLOYEE_POOL[employee_name]["discovered"] = True
        return True
    return False
