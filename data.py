"""Oyun durumu ve sabit veri sözlükleri."""

from __future__ import annotations

from typing import Any, Dict

# 1. İK Aday Havuzu (Personel Kartları)
EMPLOYEE_POOL: Dict[str, Dict[str, Any]] = {
    "Arda": {
        "role": "Makine Operatörü",
        "skill": 85,
        "cost": 3000,
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
        "cost": 4000,
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
        "cost": 2500,
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
        "cost": 5000,
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
        "cost": 3200,
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
        "cost": 2800,
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
        "cost": 4200,
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
        "cost": 3500,
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
        "cost": 3800,
        "avatar": "⚡",
        "hidden_trait": "Energy Saver",
        "trait_description": (
            "Energy Saver: Kerem enerji kaybını azaltır, süreçleri dengeler (Pozitif etki)."
        ),
        "discovered": False,
    },
}

# 2. Level ve Kriz Verileri
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {
        "name": "Level 1: Peak Hour Chaos",
        "crisis_name": "Üretim Hattında Darboğaz!",
        "description": "İlk ekip seçimi zamanı. Sınırlı bütçeyle en uygun üç adayı belirle.",
        "stations": ["İstasyon 1", "İstasyon 2"],
        "budget": 9000,
        "bonus_budget": 0,
        "candidates": ["Arda", "Merve", "Can", "Selin"],
        "progress_target": 0.35,
    },
    2: {
        "name": "Level 2: Expansion Shift",
        "crisis_name": "Kalite Sapması Alarmı!",
        "description": "Yeni vardiya açıldı. Daha yetenekli adaylarla ekibi genişlet.",
        "stations": ["İstasyon 1", "İstasyon 2"],
        "budget": 12000,
        "bonus_budget": 2000,
        "candidates": [
            "Arda",
            "Merve",
            "Can",
            "Mina",
            "Emre",
            "Selin",
            "Bora",
            "Zeynep",
            "Kerem",
        ],
        "progress_target": 0.7,
    },
}


def discover_employee_trait(employee_name: str) -> bool:
    """Bir personelin gizli özelliğini 'keşfedildi' olarak işaretler."""
    if employee_name in EMPLOYEE_POOL:
        EMPLOYEE_POOL[employee_name]["discovered"] = True
        return True
    return False
