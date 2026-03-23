# 🕵️ OpenClaw-Style AI Research Agent

An autonomous AI agent that performs real-time internet research on founders/CEOs, gathers information from multiple sources, maintains memory, and generates structured insights — powered entirely by a **local LLM (phi3 via Ollama)** with **zero API dependency**.

---

## 🚀 Features

- 🔍 Autonomous web exploration (search + browsing)
- 🌐 Multi-source information gathering
- 🧠 Memory-based reasoning across steps
- 🧹 Content filtering & validation (reduces hallucination)
- 📊 Structured output generation (biography format)
- ⚡ Fully local execution (no API keys required)
- 🎯 Streamlit UI for interactive usage

---

## 🧠 Architecture
```text
User Input
↓
Planner (Task Generation)
↓
Search Tool (DuckDuckGo)
↓
Web Scraper (BeautifulSoup)
↓
Content Validation
↓
LLM (phi3 via Ollama)
↓
Memory Storage
↓
Final Structured Output
```

---

## 🛠️ Tech Stack

- **Python**
- **Ollama (phi3 model)** – Local LLM
- **DuckDuckGo Search (ddgs)**
- **BeautifulSoup** – Web scraping
- **Streamlit** – UI
- **JSON** – Output storage

---

## 📁 Project Structure
```text
openclaw-agent/
│── tools.py # Search + scraping + validation
│── memory.py # Memory management
│── agent.py # Core agent logic
│── app.py # Streamlit UI
│── output.json # Generated results
│── README.md
```

---

## ▶️ Usage
1. Enter a founder/CEO name (e.g., Sam Altman)
2. Click Run Agent
3. The agent will:
- Search web sources
- Extract relevant content
- Analyze using local LLM
- Store insights in memory
- Generate structured summary

---

## 🧠 Key Design Decisions
❌ Avoided external APIs → ensures privacy + cost-free usage \
✅ Used strict prompting → reduces hallucination \
✅ Implemented content validation → improves accuracy \
✅ Multi-source aggregation → better factual reliability

---

## ⚠️ Limitations
- Dependent on publicly available web data \
- Local models (phi3) may be less accurate than large cloud LLMs \
- Some websites may block scraping

---

## 🔥 Future Improvements
✅ Fact-checking layer (cross-source verification) \
✅ Better ranking of sources \
✅ Advanced UI dashboard \
✅ Multi-agent architecture

---

## 👨‍💻 Author

Vedant Patil \
AI & Data Science Undergraduate

---

## ⭐ If you found this useful

### Give a ⭐ on GitHub and share your feedback!