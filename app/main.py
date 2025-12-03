import streamlit as st
from io import BytesIO

from parser import extract_text_from_pdf, extract_text_from_docx
from analyzer import calculate_score
from utils import normalize_text

st.set_page_config(
    page_title="AI Resume Quality Checker (Lite)",
    page_icon="✅",
    layout="centered",
)

st.title("AI Resume Quality Checker (Lite)")
st.write(
    "Upload your resume as PDF or DOCX. "
    "The app will detect key sections and give you a simple quality score."
)

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Dosya içeriğini memory'e al
    file_bytes = BytesIO(uploaded_file.read())

    # Dosya türüne göre metni çıkar
    if uploaded_file.name.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
    elif uploaded_file.name.lower().endswith(".docx"):
        raw_text = extract_text_from_docx(file_bytes)
    else:
        st.error("Only PDF and DOCX files are supported.")
        st.stop()

    if not raw_text or not raw_text.strip():
        st.error("Could not extract any text from this file.")
        st.stop()

    # --- Preview ---
    st.subheader("Extracted Text Preview 👇")
    st.text_area("Resume Text", raw_text[:3000], height=250)

    # --- Skor ve feedback ---
    score, feedback, sections = calculate_score(raw_text)

    st.subheader("Score Result:")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Quality Score", f"{score} %")
        st.progress(score / 100)

    with col2:
        st.write("**Detected Sections**")
        st.write("✅ Education" if sections.get("education") else "❌ Education")
        st.write("✅ Experience" if sections.get("experience") else "❌ Experience")
        st.write("✅ Skills" if sections.get("skills") else "❌ Skills")

    st.subheader("Feedback:")
    if not feedback:
        st.write("Looks good! No major issues detected.")
    else:
        for msg in feedback:
            st.write("• " + msg)