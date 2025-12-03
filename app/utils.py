SECTION_KEYWORDS = {
    "education": [
        # İngilizce
        "education", "education background", "educational background",
        "education history", "academic background",
        # Türkçe 
        "eğitim", "eğitim bilgileri", "eğitim durumu",
        "egitim", "egitim bilgileri", "egitim durumu",
        "öğrenim durumu", "ogrenim durumu",
        "lisans", "yüksek lisans", "yuksek lisans"
    ],
    "experience": [
        # İngilizce
        "experience", "work experience", "professional experience",
        "employment history", "job experience", "internship", "internships",
        # Türkçe
        "iş deneyimi", "is deneyimi", "deneyim", "deneyimler",
        "çalışma deneyimi", "calisma deneyimi",
        "staj", "staj deneyimi"
    ],
    "skills": [
        # İngilizce
        "skills", "technical skills", "soft skills", "key skills",
        # Türkçe
        "yetenekler", "beceriler", "teknik beceriler",
        "yetenek", "beceri"
    ],
}

TECH_KEYWORDS = [
    "python", "java", "c++", "c#", "javascript", "typescript",
    "html", "css", "react", "angular", "vue",
    "spring", "spring boot", "django", "flask",
    "sql", "postgresql", "mysql", "mariadb",
    "git", "github", "docker", "kubernetes",
    "machine learning", "deep learning", "data analysis",
    "rest api", "microservices"
]


def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.lower().split())