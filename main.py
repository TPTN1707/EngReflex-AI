import streamlit as st
from src.services.groq_service import run_checker_agent, run_explainer_agent, run_chat_partner_agent
# Import the initial greeting helper to support resetting conversations on scenario change
from src.prompts.chat_partner import get_initial_greeting

# Page configuration
st.set_page_config(
    page_title="EngReflex AI - Writing Reflex Trainer",
    page_icon="✍️",
    layout="wide"
)

# App Header
st.title("✍️ EngReflex AI")
st.subheader("Your AI Reflex Gym to eliminate Vietnamese-translation habits")
st.write("---")

# ==========================================
# SIDEBAR CONFIGURATION (Arena Control)
# ==========================================
st.sidebar.title("🛠️ Arena Configuration")

# Selection for writing scenario
scenario = st.sidebar.selectbox(
    "Select Writing Scenario:",
    options=["casual", "business", "interview"],
    format_func=lambda x: {
        "casual": "💬 Casual Chat (Friendly & Relaxed)",
        "business": "👔 Business Email (Professional Workplace)",
        "interview": "💼 Job Interview (HR Recruiter Panel)"
    }[x]
)

# Selection for tutor explanation language
explanation_level_c = st.sidebar.selectbox(
    "Tutor Explanation Language:",
    options=["vietnamese", "bilingual", "simple_english"],
    format_func=lambda x: {
        "vietnamese": "🇻🇳 Pure Vietnamese",
        "bilingual": "🇬🇧🇻🇳 Bilingual English-Vietnamese",
        "simple_english": "🇬🇧 Simple English (A2-B1 level)"
    }[x]
)

# ==========================================
# CHAT RESET LOGIC (Triggered on Scenario Change)
# ==========================================
# Initialize scenario state tracker
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = scenario

# If user changes scenario in sidebar, reset chat history and tutor panel instantly
if st.session_state.current_scenario != scenario:
    st.session_state.current_scenario = scenario
    # Load the fresh scenario-specific greeting
    st.session_state.chat_history = [
        {"role": "model", "parts": [{"text": get_initial_greeting(scenario)}]}
    ]
    st.session_state.latest_tutor_feedback = None
    st.rerun()

# Initial session state initialization for first boot
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "model", "parts": [{"text": get_initial_greeting(scenario)}]}
    ]
if "latest_tutor_feedback" not in st.session_state:
    st.session_state.latest_tutor_feedback = None

# ==========================================
# DUAL-COLUMN CHAT ARENA LAYOUT
# ==========================================
col_chat_ui, col_tutor_ui = st.columns([5, 4])

# Left Column: Chat Messenger Interface
with col_chat_ui:
    st.markdown(f"### 💬 Chat Messenger ({scenario.capitalize()} Mode)")
    st.write("---")

    # Container to show scrollable chat messages
    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state.chat_history:
            role = "assistant" if message["role"] == "model" else "user"
            with st.chat_message(role):
                st.write(message["parts"][0]["text"])

    # Chat Input at the bottom of the column
    if chat_input := st.chat_input("Type your response here in English..."):
        # 1. Display and append user's response to history
        with chat_container:
            with st.chat_message("user"):
                st.write(chat_input)
        st.session_state.chat_history.append({"role": "user", "parts": [{"text": chat_input}]})

        # 2. Trigger Checker & Explainer Agents in the background on user's message
        check_result = run_checker_agent(chat_input)
        if "error" not in check_result and check_result.get("errors"):
            # Run the explainer if errors are found
            explanation = run_explainer_agent(check_result, level=explanation_level_c)
            st.session_state.latest_tutor_feedback = {
                "check_result": check_result,
                "explanation": explanation
            }
        else:
            # Clear or set empty feedback if message is perfectly clean
            st.session_state.latest_tutor_feedback = {
                "clean": True,
                "original_text": chat_input
            }

        # 3. Call Chat Partner Agent to generate the next response passing the selected scenario
        with st.spinner("Typing response..."):
            ai_response = run_chat_partner_agent(st.session_state.chat_history, scenario=scenario)
        
        # 4. Append AI response to history and rerun to update UI
        st.session_state.chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
        st.rerun()

# Right Column: Real-time Tutor Panel
with col_tutor_ui:
    st.markdown("### 💡 Real-Time Tutor Panel")
    st.write("This panel analyzes your *very last* sent message in real-time.")
    st.write("---")

    feedback = st.session_state.latest_tutor_feedback
    if feedback:
        if feedback.get("clean"):
            st.balloons()
            st.success(f"✨ **Perfect Response!**\n\nYour message: *\"{feedback['original_text']}\"* is highly natural and grammatically correct!")
        else:
            check_res = feedback["check_result"]
            
            # Show corrections and suggestions
            st.markdown("#### 📝 Corrections")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.info(f"**What you said:**\n\n *\"{check_res['original_text']}\"*")
            with col_c2:
                st.success(f"**Grammar Fix:**\n\n *\"{check_res['corrected_text']}\"*")
            
            # Show native suggestions
            native_style = check_res.get("native_rephrased", "")
            if native_style:
                st.info(f"✨ **Native Speaker Style:**\n\n *\"{native_style}\"*")

            # Show detailed breakdown
            st.markdown("#### 🔍 Tutor's Analysis")
            st.write(feedback["explanation"])
    else:
        st.info("Send a message in the chat to start receiving real-time tutor feedback.")