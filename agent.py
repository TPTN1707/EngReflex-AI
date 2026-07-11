import os
import json
from dotenv import load_dotenv
from groq import Groq
from google import genai
from google.genai import types
from prompts import CHECKER_PROMPT, get_explainer_prompt

# Load environment variables
load_dotenv()

# Verify that API keys are loaded properly
gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not gemini_key or not groq_key:
    print("Warning: Missing GEMINI_API_KEY or GROQ_API_KEY in .env file.")

# Initialize API clients
groq_client = Groq(api_key=groq_key)
gemini_client = genai.Client(api_key=gemini_key)

def run_checker_agent(text_input):
    """Call Groq to perform rapid grammar and Viet-lish checks"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": CHECKER_PROMPT},
                {"role": "user", "content": text_input}
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": f"Checker Agent Error: {str(e)}"}

def run_explainer_agent(error_details, level="vietnamese"):
    """Call Gemini to explain errors using the active gemini-2.0-flash model"""
    # Using gemini-2.0-flash based on your active API model list
    target_model = 'gemini-2.0-flash'
    try:
        response = gemini_client.models.generate_content(
            model=target_model,
            contents=f"Please explain these errors:\n{json.dumps(error_details, ensure_ascii=False)}",
            config=types.GenerateContentConfig(
                system_instruction=get_explainer_prompt(level)
            )
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        # Diagnostics: Safe model listing in case of future model mismatches
        if "404" in error_msg or "NOT_FOUND" in error_msg:
            print(f"\n[Diagnostic] Model '{target_model}' failed. Listing your available models:")
            try:
                models = gemini_client.models.list()
                for m in models:
                    print(f" - {m.name}")
            except Exception as list_err:
                print(f"Could not list models: {str(list_err)}")
        return f"Explainer Agent Error: {error_msg}"

if __name__ == "__main__":
    test_sentence = "My family has 4 people, and I make research about AI."
    print("--- RUNNING CHECKER AGENT (GROQ) ---")
    check_result = run_checker_agent(test_sentence)
    print(json.dumps(check_result, indent=2, ensure_ascii=False))
    
    if "error" not in check_result:
        print("\n--- RUNNING EXPLAINER AGENT (GEMINI) ---")
        explanation = run_explainer_agent(check_result["errors"], level="vietnamese")
        print(explanation)