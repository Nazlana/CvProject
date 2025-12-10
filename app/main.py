import streamlit as st
from io import BytesIO
import base64
from parser import extract_text_from_pdf, extract_text_from_docx
from analyzer import calculate_score

# Font Awesome CDN
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="CV Quality Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS

# Title and Description
st.markdown("""
    <div class='header'>
        <h1><i class="fas fa-file-invoice"></i> CV Quality Checker</h1>
        <p>Upload your CV, get it analyzed automatically, and receive improvement suggestions</p>
    </div>
""", unsafe_allow_html=True)

# File Upload Section
with st.container():
    st.markdown("""<h3><i class="fas fa-upload"></i> Upload Your CV</h3>""", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload CV",
        type=["pdf", "docx"],
        key="file_uploader",
        label_visibility="collapsed"
    )
    st.info("Drag and drop or click to upload your CV. Only PDF and DOCX formats are supported.", icon="ℹ️")

if uploaded_file is not None:
    with st.spinner('Analyzing your CV, please wait...'):
        # Dosya içeriğini oku
        file_bytes = BytesIO(uploaded_file.read())

        # Dosya türüne göre metni çıkar
        try:
            if uploaded_file.name.lower().endswith(".pdf"):
                raw_text = extract_text_from_pdf(file_bytes)
            else:
                raw_text = extract_text_from_docx(file_bytes)

            if not raw_text or not raw_text.strip():
                st.error("Could not extract text from the file. Please try a different file.")
                st.stop()

            # Get analysis results
            score, feedback, sections = calculate_score(raw_text)

            # Display results
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("### <i class='fas fa-chart-line' style='color:#2e4bb4;'></i> Analiz Sonuçları", unsafe_allow_html=True)
                
                # Score card
                with st.container():
                    st.markdown(f"""
                    <div class='score-card'>
                        <h3>Overall Score: {score}/100</h3>
                        <div style='height: 10px; margin: 10px 0;'>
                    """, unsafe_allow_html=True)
                    st.progress(score / 100)
                    st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Detected sections
                st.markdown("### <i class='fas fa-list-check' style='color:#2e4bb4;'></i> Detected Sections", unsafe_allow_html=True)
                cols = st.columns(3)
                section_icons = {
                    "education": "<i class='fas fa-graduation-cap' style='color:#2e4bb4;'></i>",
                    "experience": "<i class='fas fa-briefcase' style='color:#2e4bb4;'></i>",
                    "skills": "<i class='fas fa-screwdriver-wrench' style='color:#2e4bb4;'></i>"
                }
                
                for i, (section, found) in enumerate(sections.items()):
                    with cols[i % 3]:
                        icon = section_icons.get(section, "<i class='fas fa-thumbtack'></i>")
                        status = (
                            "<i class='fas fa-circle-check' style='color:#16a34a;'></i>"
                            if found
                            else "<i class='fas fa-circle-xmark' style='color:#dc2626;'></i>"
                        )
                        st.markdown(f"""
                        <div class='section-card'>
                            <h4>{status} {icon} {section.capitalize()}</h4>
                        </div>
                        """, unsafe_allow_html=True)

            with col2:
                # Quick Summary
                st.markdown("### <i class='fas fa-clipboard-list' style='color:#2e4bb4;'></i> Quick Summary", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background: #f0f7ff; padding: 1rem; border-radius: 10px;'>
                    <p><b>File Name:</b> {uploaded_file.name}</p>
                    <p><b>Character Count:</b> {len(raw_text):,}</p>
                    <p><b>Sections Found:</b> {sum(1 for x in sections.values() if x)}/3</p>
                </div>
                """, unsafe_allow_html=True)

                # Download button
                st.download_button(
                    label="⬇️ Download Analysis Results",
                    data=f"CV Analysis Result\nScore: {score}/100\n\nDetected Sections:\n" + 
                         "\n".join([f"- {k.capitalize()}: {'✅ Found' if v else '❌ Missing'}" for k, v in sections.items()]) +
                         "\n\nSuggestions:\n" + "\n".join([f"- {msg}" for msg in (feedback if feedback else ["Great job! No major issues detected."])]),
                    file_name="cv_analysis_result.txt",
                    mime="text/plain"
                )

            # Feedback
            st.markdown("### <i class='fas fa-lightbulb' style='color:#f59e0b;'></i> Improvement Suggestions", unsafe_allow_html=True)
            if not feedback:
                st.success("Congratulations! Your CV looks good overall. No major issues were detected.")
            else:
                for msg in feedback:
                    st.markdown(f"<div class='feedback-item'>{msg}</div>", unsafe_allow_html=True)

            # Raw text preview (collapsible)
            with st.expander("🗂️ View Extracted Text", expanded=False):
                st.text_area("Extracted Text", raw_text, height=300, disabled=True, key="raw_text_area")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.stop()

# Sidebar
with st.sidebar:
    sidebar_content = """
    <div class="custom-sidebar">
        <div class="sidebar-header"><h2 style="font-size:28px; line-height:1.2; margin:0;"><i class="fas fa-info-circle" style="color:#2e4bb4;"></i> Information</h2>
        <p>This application checks the key sections of your CV and provides improvement suggestions.
        <p><div class="sidebar-header"><h3 style="font-size:22px; line-height:1.2; margin:0;"><i class="fas fa-tasks" style="color:#2e4bb4;"></i>   What's Checked:</h3></div></p>
        <p><div class="sidebar-item"><i class="fas fa-graduation-cap"></i> Education Information</div></p>
        <p><div class="sidebar-item"><i class="fas fa-briefcase"></i> Work Experience</div></p>
        <p><div class="sidebar-item"><i class="fas fa-cogs"></i> Skills and Competencies</div></p>
        <p><div class="sidebar-header"><h3 style="font-size:22px; line-height:1.2; margin:0;"><i class="fas fa-rocket" style="color:#2e4bb4;"></i>   How to Use</h3></div></p>
        <p><div class="sidebar-item"><i class="fas fa-upload"></i> Upload your CV (PDF or DOCX)</div></p>
        <p><div class="sidebar-item"><i class="fas fa-search-plus"></i> Review the analysis results</div></p>
        <p><div class="sidebar-item"><i class="fas fa-edit"></i> Update your CV based on suggestions</div></p>
        <p><div class="sidebar-item"><i class="fas fa-shield-alt"></i><b>Privacy Note:</b> Your uploaded files are not stored on our servers.</div></p> </p>
        
        
    </div>
    """
    st.markdown(sidebar_content, unsafe_allow_html=True)