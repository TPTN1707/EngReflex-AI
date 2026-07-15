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

EngReflex AI runs entirely on the ultra-fast **Groq Cloud API** using a dual-agent configuration:
1. **Checker Agent:** Runs **`llama-3.3-70b-versatile`** to perform fast, highly logical grammatical checks and output structured JSON.
2. **Explainer Agent:** Runs **`llama-3.3-70b-versatile`** for deep, context-aware bilingual linguistic explanations.
3. **Chat Partner Agent:** Runs **`llama-3.1-8b-instant`** for low-latency, engaging everyday conversation.

## 💻 Getting Started

### Prerequisites
You only need a single free API key for this project:
- A **Groq API Key** from the [Groq Console](https://console.groq.com/).

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

### Running the Application

To start the local Streamlit web application, run the following command:

    streamlit run main.py

The application will automatically open in a new tab in your default browser (usually at http://localhost:8501).