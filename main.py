import streamlit as st
from agent import run_checker_agent, run_explainer_agent

# Page configuration
st.set_page_config(
    page_title="EngReflex AI - Writing Reflex Trainer",
    page_icon="✍️",
    layout="centered"
)

# App Header
st.title("✍️ EngReflex AI")
st.subheader("Your AI Reflex Gym to eliminate Vietnamese-translation habits")
st.write("Write naturally in English, identify literal translation patterns, and learn actively.")

# User Input Section
user_text = st.text_area(
    "Enter your English writing below:",
    height=150,
    placeholder="e.g., My family has 4 people, and I make research about AI."
)

# Configuration Options
col1, col2 = st.columns([2, 1])
with col1:
    explanation_level = st.selectbox(
        "Choose explanation level:",
        options=["vietnamese", "bilingual", "simple_english"],
        format_func=lambda x: {
            "vietnamese": "🇻🇳 Pure Vietnamese (For quick conceptual understanding)",
            "bilingual": "🇬🇧🇻🇳 Bilingual English-Vietnamese",
            "simple_english": "🇬🇧 Simple English (A2-B1 Level - Recommended for immersion)"
        }[x]
    )

# Execution Trigger
if st.button("Analyze & Train", type="primary"):
    if not user_text.strip():
        st.warning("Please enter some English text before training.")
    else:
        # Step 1: Run the Checker Agent
        with st.spinner("Analyzing grammar and translation habits..."):
            check_result = run_checker_agent(user_text)
        
        if "error" in check_result:
            st.error(check_result["error"])
        else:
            st.success("Analysis Complete!")
            
            # Display original vs corrected text
            st.markdown("### 📝 Corrections")
            col_orig, col_corr = st.columns(2)
            with col_orig:
                st.info(f"**Original Text:**\n\n {check_result['original_text']}")
            with col_corr:
                st.success(f"**Suggested Text (Grammatically Correct):**\n\n {check_result['corrected_text']}")
            
            # Display Native Speaker Rephrasing
            native_style = check_result.get("native_rephrased", "")
            if native_style:
                st.info(f"✨ **Native Speaker Style (Highly Natural):**\n\n *\"{native_style}\"*")
            
            # Display detailed errors list if any
            errors_list = check_result.get("errors", [])
            if errors_list:
                st.markdown("### 🔍 Detected Patterns")
                for err in errors_list:
                    incorrect = err.get("incorrect", "N/A")
                    correct = err.get("correct", "N/A")
                    err_type = err.get("type", "Error")
                    
                    st.markdown(f"- **Type:** `{err_type}` | **Incorrect:** `\"{incorrect}\"` ➡️ **Correct:** `\"{correct}\"`")
                
                # Step 2: Run the Explainer Agent with FULL check_result context
                st.markdown("### 💡 Tutor's Explanation & Analysis")
                with st.spinner("Generating tailored explanation..."):
                    # Pass the whole check_result dictionary
                    explanation = run_explainer_agent(check_result, level=explanation_level)
                
                st.write(explanation)
            else:
                st.balloons()
                st.info("Excellent! No obvious grammar or translation patterns detected.")