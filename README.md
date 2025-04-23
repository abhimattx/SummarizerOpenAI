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
<div align="center">
  <a href="assets/summarizer(1).mp4" target="_blank">
    <img src="assets/thumbnail.png" alt="Demo Video Thumbnail" width="600"/>
    <br>
    <b>▶️ Click to download and watch demo</b>
  </a>
</div>
---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/openai-summarizer.git

cd openai-summarizer
```

### 2. Add your API key (local only)

Create `.streamlit/secrets.toml` and paste:

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
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

📁 Folder Structure

```
SummarizerOpenAI/
├── app.py                  # Streamlit UI
├── openai_api.py           # GPT summarizer logic
├── file_handler.py         # File upload reading logic
├── requirements.txt
├── .gitignore
├── README.md
├── .streamlit/
│   └── secrets.toml.example
└── assets/
```

---

📦 Requirements

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
