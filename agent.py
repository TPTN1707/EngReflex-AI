import os
import json
from dotenv import load_dotenv
from groq import Groq
from google import genai
from google.genai import types
from prompts import CHECKER_PROMPT, get_explainer_prompt

# Load environment variables from .env file
load_dotenv()

# Initialize API clients for Groq and Gemini
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def run_checker_agent(text_input):
    """
    Call Groq API to analyze English text for spelling, grammar, and Viet-lish errors.
    Returns a structured JSON object containing corrections and error types.
    """
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": CHECKER_PROMPT},
                {"role": "user", "content": text_input}
            ],
            model="llama-3.1-8b-instant", # Active fast model on Groq
            response_format={"type": "json_object"} # Enforce strict JSON output
        )
        # Parse the raw JSON string from the response into a Python dictionary
        result = json.loads(chat_completion.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": f"Checker Agent Error: {str(e)}"}

def run_explainer_agent(error_details, level="vietnamese"):
    """
    Call Gemini API using the new google-genai SDK to explain errors.
    Supports three levels: vietnamese, bilingual, and simple_english.
    """
    try:
        # Use gemini-1.5-flash as the stable free-tier model
        response = gemini_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Please explain these errors:\n{json.dumps(error_details, ensure_ascii=False)}",
            config=types.GenerateContentConfig(
                system_instruction=get_explainer_prompt(level)
            )
        )
        return response.text
    except Exception as e:
        return f"Explainer Agent Error: {str(e)}"

# Local testing block to verify API integrations
if __name__ == "__main__":
    test_sentence = "My family has 4 people, and I make research about AI."
    print("--- RUNNING CHECKER AGENT (GROQ) ---")
    check_result = run_checker_agent(test_sentence)
    print(json.dumps(check_result, indent=2, ensure_ascii=False))
    
    if "error" not in check_result:
        print("\n--- RUNNING EXPLAINER AGENT (GEMINI) ---")
        explanation = run_explainer_agent(check_result["errors"], level="vietnamese")
        print(explanation)