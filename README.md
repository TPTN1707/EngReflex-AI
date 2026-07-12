# EngReflex AI ✍️

EngReflex AI is an active English writing reflex trainer designed specifically for Vietnamese learners. Rather than being a passive autocorrect tool, it acts as an interactive "Reflex Gym" to help users eliminate literal translation habits (Viet-lish), learn natural collocations, and transition from passive English knowledge to active writing fluency.

The project utilizes a fast, cost-effective **dual-API multi-agent architecture** running entirely on free-tier services.

---

## 🚀 Key Features

- **Literal Translation (Viet-lish) Detection:** Specifically flags sentences that are grammatically correct but structured with Vietnamese thinking patterns (literal translations).
- **High-Precision Minimal Span Error Correction:** Isolates and corrects spelling, grammar, and punctuation errors accurately without corrupting adjacent correct words.
- **✨ Native Speaker Style Rephrasing:** Generates highly natural, idiomatic alternatives that native speakers actually use (e.g., transforming *"My family has four people"* into *"There are four people in my family"*).
- **💡 Tutor's Explanation & Analysis:**
  - **Error Corrections:** Plain explanations of grammatical issues in the selected language.
  - **Native Style Analysis:** Explains the lexical choices and idiomatic nuances of the native rephrased version.
  - **Structure & Tense Analysis:** Compares the tenses and clause patterns of both the corrected and native versions.
- **Graduated Explanations:** Allows users to choose between Pure Vietnamese, Bilingual, or Simple English explanations depending on their learning stage.

---

## 🛠️ Tech Stack & Architecture

EngReflex AI uses an on-demand sequential pipeline to save API tokens and minimize latency:

1. **Frontend:** [Streamlit](https://streamlit.io/) (Python-based interactive web UI).
2. **Checker Agent:** [Groq Cloud API](https://groq.com/) running **`llama-3.3-70b-versatile`** to perform fast, highly logical grammatical checks and output structured JSON.
3. **Explainer Agent:** [Google Gemini API](https://ai.google.dev/) running **`gemini-flash-latest`** via the new `google-genai` SDK for deep, context-aware bilingual linguistic explanations.

---

## 📁 Project Directory Structure

```text
EngReflex-AI/
├── .env                  # Local environment variables (API keys)
├── .gitignore            # Git exclusion configuration
├── pyproject.toml        # Dependency management file (managed by uv)
├── prompts.py            # System prompts for Checker and Explainer agents
├── agent.py              # Backend API orchestration logic
├── main.py               # Streamlit web application interface
└── README.md             # Project documentation
```

---

## 💻 Getting Started

### Prerequisites

You will need the following API keys (both have generous free tiers):
1. A **Groq API Key** from [Groq Console](https://console.groq.com/).
2. A **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

---

### Running the Application

To start the local Streamlit web application, run the following command:

    streamlit run main.py

The application will automatically open in a new tab in your default browser (usually at http://localhost:8501).