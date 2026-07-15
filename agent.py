import os
import json
from dotenv import load_dotenv
from groq import Groq
from google import genai
from google.genai import types
from prompts import CHECKER_PROMPT, get_explainer_prompt, CHAT_PARTNER_PROMPT

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
    """Call Groq using llama-3.3-70b-versatile for high-precision grammar logic"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": CHECKER_PROMPT},
                {"role": "user", "content": text_input}
            ],
            model="llama-3.3-70b-versatile", 
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": f"Checker Agent Error: {str(e)}"}

def run_explainer_agent(check_result, level="vietnamese"):
    """Call Gemini using the newer, less congested gemini-2.0-flash-lite model"""
    # Switched to 2.0-flash-lite to avoid the 503 spikes of the standard 1.5-flash
    target_model = 'gemini-2.0-flash-lite'
    try:
        response = gemini_client.models.generate_content(
            model=target_model,
            contents=f"Please explain and analyze this writing analysis data:\n{json.dumps(check_result, ensure_ascii=False)}",
            config=types.GenerateContentConfig(
                system_instruction=get_explainer_prompt(level)
            )
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "NOT_FOUND" in error_msg:
            print(f"\n[Diagnostic] Model '{target_model}' failed. Listing your available models:")
            try:
                models = gemini_client.models.list()
                for m in models:
                    print(f" - {m.name}")
            except Exception as list_err:
                print(f"Could not list models: {str(list_err)}")
        return f"Explainer Agent Error: {error_msg}"

def run_chat_partner_agent(chat_history):
    """
    Call Groq using llama-3.1-8b-instant to generate the next response.
    This guarantees lightning-fast chat speed and avoids Gemini's free-tier 503 limits.
    """
    try:
        # Convert Gemini's chat history schema into Groq's OpenAI-compatible message format
        messages = [{"role": "system", "content": CHAT_PARTNER_PROMPT}]
        for msg in chat_history:
            role = "assistant" if msg["role"] == "model" else "user"
            text = msg["parts"][0]["text"]
            messages.append({"role": role, "content": text})

        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant" # Very fast, low latency, highly stable
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Chat Partner Error: {str(e)}"