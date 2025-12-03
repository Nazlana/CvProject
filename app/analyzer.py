from typing import Dict, List, Tuple
from utils import SECTION_KEYWORDS, TECH_KEYWORDS, normalize_text


def detect_sections(text: str) -> Dict[str, bool]:
    """
    CV içinde education / experience / skills bölümleri var mı diye
    basit keyword araması yapar.
    """
    text_norm = normalize_text(text)
    result: Dict[str, bool] = {}

    for section_name, keywords in SECTION_KEYWORDS.items():
        result[section_name] = any(kw in text_norm for kw in keywords)

    return result


def count_tech_keywords(text: str) -> int:
    """
    Metinde geçen teknik anahtar kelime sayısını döndürür.
    """
    text_norm = normalize_text(text)
    return sum(1 for kw in TECH_KEYWORDS if kw in text_norm)


def calculate_score(text: str) -> Tuple[int, List[str], Dict[str, bool]]:
    """
    Rule-based skor hesaplama ve feedback üretme.
    Skor: 0–100
    """
    feedback: List[str] = []

    text_norm = normalize_text(text)
    sections = detect_sections(text_norm)
    tech_count = count_tech_keywords(text_norm)
    word_count = len(text_norm.split())

    score = 0

    # ---- Bölüm ağırlıkları ----
    if sections.get("education"):
        score += 25
    else:
        feedback.append(
            "Add an Education section with your degree, school and graduation year."
        )

    if sections.get("experience"):
        score += 45
    else:
        feedback.append(
            "Add a Work Experience section with job titles, company names and dates."
        )

    if sections.get("skills"):
        score += 30
    else:
        feedback.append(
            "Add a Skills section listing your technical and soft skills."
        )

    # ---- Teknik keyword katkısı (maks +10, min 0) ----
    if tech_count == 0:
        feedback.append(
            "No technical skills detected (e.g. Python, Java, SQL). Add them clearly under Skills."
        )
    elif 1 <= tech_count <= 3:
        score += 3
        feedback.append(
            "Some technical skills detected; consider adding a few more relevant technologies."
        )
    elif 4 <= tech_count <= 7:
        score += 7
        feedback.append("Your technical skills look solid.")
    else:
        score += 10
        feedback.append("Strong variety of technical skills found.")

    # ---- Uzunluk kontrolü (hafif ceza/bonus) ----
    # Çok kısa CV'ler için -10, ideal aralık için +5 bonus
    if word_count < 120:
        score -= 10
        feedback.append(
            "Your resume is very short; add more details about your experience and projects."
        )
    elif 120 <= word_count <= 600:
        score += 5  # okunabilir, dolu CV'ye ufak ödül
    elif word_count > 900:
        feedback.append(
            "Your resume is quite long; consider making it more concise."
        )

    # Skoru 0–100 aralığına sıkıştır
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    # Aynı feedback tekrar etmesin
    feedback = list(dict.fromkeys(feedback))

    return score, feedback, sections

