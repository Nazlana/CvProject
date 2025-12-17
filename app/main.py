import streamlit as st
from io import BytesIO
import base64
from parser import extract_text_from_pdf, extract_text_from_docx
from analyzer import calculate_score

# Sayfa ayarları
st.set_page_config(
    page_title="CV Quality Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS ekle
st.markdown('''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Ana içerik düzeni */
        .main .block-container {
            padding: 2rem 2rem 2rem 3rem;
            max-width: 100%;
        }
        
        /* Sidebar genişliği */
        section[data-testid="stSidebar"] {
            width: 300px !important;
            min-width: 300px !important;
            padding: 1.5rem;
            background: #f8f9fa;
        }
        
        /* Header stilleri */
        .header {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: #f0f7ff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #2e4bb4;
            margin-bottom: 0.5rem;
        }
        
        /* Kart stilleri */
        .score-card, .section-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Buton stilleri */
        .stButton>button {
            width: 100%;
            margin: 5px 0;
            background-color: #2e4bb4;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        
        .stButton>button:hover {
            background-color: #1e3a8a;
        }
        
        /* Sekme stilleri */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        /* Responsive düzen */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
            section[data-testid="stSidebar"] {
                width: 250px !important;
                min-width: 250px !important;
            }
        }
    </style>
''', unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='header'>
        <h1><i class="fas fa-file-invoice"></i> CV Quality Checker</h1>
        <p>Upload your CV, get it analyzed automatically, and receive improvement suggestions</p>
    </div>
""", unsafe_allow_html=True)

# File Upload Section
with st.container():
    st.markdown("""<h3 style='color: #2e4bb4;'><i class="fas fa-upload"></i> Upload Your CV</h3>""", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload CV",
        type=["pdf", "docx"],
        key="file_uploader",
        label_visibility="collapsed"
    )
    if not uploaded_file:
        st.info("Drag and drop or click to upload your CV. Only PDF and DOCX formats are supported.", icon="ℹ️")

if uploaded_file is not None:
    with st.spinner('Analyzing your CV, please wait...'):
        # read file description
        file_bytes = BytesIO(uploaded_file.read())

        # Expert text for file type
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
# Sidebar content
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #2e4bb4; margin-bottom: 1rem;'><i class='fas fa-info-circle'></i> Information</h2>
        <p style='font-size: 1rem; line-height: 1.6;'>This application checks the key sections of your CV and provides improvement suggestions.
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
    """, unsafe_allow_html=True)
    st.markdown("""
        <div style='margin-top: 2rem;'>
            <h3 style='color: #2e4bb4; margin-bottom: 1rem;'><i class='fas fa-question-circle'></i> How It Works</h3>
            <ol style='padding-left: 1.2rem; margin-bottom: 1.5rem; line-height: 1.8;'>
                <li>Upload your CV in PDF or DOCX format</li>
                <li>Wait for the analysis to complete</li>
                <li>Review your CV score and suggestions</li>
                <li>Download the analysis results</li>
            </ol>
            <div style='background: #e6f0ff; padding: 1rem; border-radius: 8px; margin-top: 1.5rem;'>
                <h4 style='margin-top: 0; color: #2e4bb4;'><i class='fas fa-lightbulb'></i> Tip</h4>
                <p style='margin-bottom: 0;'>For best results, make sure your CV includes clear section headings like 'Education', 'Experience', and 'Skills'.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
        
        
    </div>
    """
    st.markdown(sidebar_content, unsafe_allow_html=True)
