# CV Quality Checker

A Streamlit-based web application that analyzes CVs (PDF/DOCX) and provides quality feedback, section detection, and improvement suggestions.

## Features

- 📄 Supports PDF and DOCX file formats
- 🔍 Extracts text and analyzes CV content
- 📊 Provides a quality score (0-100)
- 🎯 Detects key sections (Education, Experience, Skills)
- 💡 Offers improvement suggestions
- 📱 Responsive design for all devices

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nazlana/CvProject.git
   cd CvProject
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

2. Open your browser and go to `http://localhost:8501`

3. Upload your CV file (PDF or DOCX) and view the analysis results

## Project Structure

```
CvProject/
├── app/
│   ├── __init__.py
│   ├── main.py         # Main Streamlit application
│   ├── analyzer.py     # CV analysis logic
│   ├── parser.py       # File parsing utilities
│   └── utils.py        # Helper functions
├── .gitignore
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
