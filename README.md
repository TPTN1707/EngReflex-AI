# EngReflex AI ✍️

EngReflex AI is an interactive, real-time English writing reflex trainer designed for Vietnamese learners. Rather than being a passive autocorrect tool, it acts as an active **"Reflex Gym"** with a clean, single-screen dual-panel interface. It helps users eliminate literal translation habits (Viet-lish), master natural collocations, and transition from passive English knowledge to active writing fluency under real-time constraints.

The project runs entirely on the ultra-fast, cost-effective **Groq Cloud API** using a highly optimized modular architecture.

---

## 🚀 Key Features

- **💬 Real-Time Chat Messenger (Left Panel):** Engage in natural, open-ended conversations with an AI companion. The AI drives the conversation to force real-time retrieval without time to translate word-by-word in your head.
- **👔 Contextual Writing Scenarios (New!):** Switch between different writing personas and contexts using the sidebar. The AI automatically adapts its vocabulary level and tone:
  - *Casual Chat:* Friendly and relaxed peer conversation using everyday A2-B1 vocabulary.
  - *Business Email:* Professional, well-structured business interactions.
  - *Job Interview:* Formal interview queries conducting situational and behavioral checks.
- **💡 Real-Time Tutor Feedback (Right Panel):** Analyzes your very last sent message instantly:
  - **📝 Corrections:** Highlights and explains spelling, grammar, and punctuation mistakes.
  - **✨ Native Speaker Style:** Suggests idiomatic, highly natural rephrasings that native speakers actually use (e.g., transforming *"My family has four people"* into *"There are four people in my family"*).
  - **🔍 Tutor's Analysis:** Explains the errors in Vietnamese and analyzes the advanced vocabulary and phrasal structures of the native version.
- **Graduated Explanations:** Choose between Pure Vietnamese, Bilingual, or Simple English explanations directly from the sidebar.

---

## 🛠️ Tech Stack & Architecture

EngReflex AI runs entirely on the ultra-fast **Groq Cloud API** using a multi-agent configuration:
1. **Checker Agent:** Runs `llama-3.3-70b-versatile` to perform fast, highly logical grammatical checks and output structured JSON.
2. **Explainer Agent:** Runs `llama-3.3-70b-versatile` for deep, context-aware bilingual linguistic explanations.
3. **Chat Partner Agent:** Runs `llama-3.1-8b-instant` for low-latency, engaging conversational roleplays based on the selected scenario.

---

## 📁 Project Directory Structure

    EngReflex-AI/
    ├── .env                         # API keys
    ├── .gitignore                   # Git ignore files
    ├── pyproject.toml               # uv package config (managed by uv)
    ├── uv.lock                      # Locked dependency versions
    ├── main.py                      # Streamlit UI entry point
    │
    └── src/                         # Main source code directory
        ├── __init__.py
        ├── config.py                # Centralized configuration and model settings
        │
        ├── prompts/                 # Modularized system prompts
        │   ├── __init__.py
        │   ├── checker.py           # Checker Agent system instructions
        │   ├── explainer.py         # Explainer Agent system instructions
        │   └── chat_partner.py      # Chat Partner Agent system instructions
        │
        └── services/                # Backend API orchestrators
            ├── __init__.py
            └── groq_service.py      # Integrated Groq API client

---

## 💻 Getting Started

### Prerequisites
You only need a single free API key for this project:
- A **Groq API Key** from the [Groq Console](https://console.groq.com/).

### Installation

This project manages packages using Astral's fast Python package installer, `uv`.

1. Navigate to your project directory:

    cd EngReflex-AI

2. Create a `.env` file in the root directory and add your API key:

    GROQ_API_KEY=your_groq_api_key_here

3. Sync and install dependencies:

    uv sync

### Running the Application

To start the local Streamlit web application, run the following command:

    uv run streamlit run main.py

The application will automatically open in a new tab in your default browser (usually at http://localhost:8501).