## 📑 GPT Text Summarizer

<div align="center">
<img alt="GPT Summarizer" src="https://img.shields.io/badge/GPT-Summarizer-12A87D?style=for-the-badge&amp;logo=openai&amp;logoColor=white">
Transform lengthy content into concise summaries powered by OpenAI's GPT models

<img alt="GitHub" src="https://img.shields.io/badge/View_on-GitHub-181717?style=for-the-badge&amp;logo=github">
<img alt="Streamlit" src="https://img.shields.io/badge/Try_it_on-Streamlit-FF4B4B?style=for-the-badge&amp;logo=streamlit">
<img alt="License" src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge">
---

## ✨ Features

- 📄 Paste text or upload files (PDF, DOCX, TXT)
- 🔍 Choose summary length: short, medium, or long
- 🔐 Use your own OpenAI API key (optional)
- 📊 See token usage and estimated cost
- 💡 Clean UI built with Streamlit
- ☁️ Deployable on Streamlit Cloud

---

## 🖼 Screenshot
> Add a preview in `assets/summarizer (1).mp4`

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/abhimattx/SummarizerOpenAI.git
cd SummarizerOpenAI

# Set up API key (create .streamlit/secrets.toml)
echo 'OPENAI_API_KEY = "your-api-key-here"' > .streamlit/secrets.toml

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo → Choose `app.py`
4. In “Secrets”, add:

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
```

Done! ✅

---

## 📁 Folder Structure

```
openai-summarizer/
│
├── app.py                  # Streamlit user interface
├── openai_api.py           # OpenAI integration and token tracking
├── file_handler.py         # Document processing for PDF/DOCX/TXT
│
├── requirements.txt        # Project dependencies
├── .streamlit/
│   └── secrets.toml.example
│
├── assets/                 # Images and static resources
└── uploads/                # Temporary file storage
```

---

## 📦 Requirements

```txt
streamlit
openai>=1.0.0
PyMuPDF           # For PDFs
python-docx       # For .docx files
tiktoken          # For token counting
pillow            # For image handling
```

---

## 💰 Cost Estimation

The app shows token usage and approximate cost:

- GPT-3.5-turbo = ~$0.0015 per 1K tokens
- Calculation is shown under each summary

---

## 🧑‍💻 Author

<div align="center"> <strong>Abhishek Singh</strong><br> <a href="https://www.linkedin.com/in/abhimattx/">LinkedIn</a> • <a href="https://github.com/abhimattx">GitHub</a> </div>

---

## 📄 License
MIT – use it, remix it, build something great!
