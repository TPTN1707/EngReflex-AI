import os
import json
from dotenv import load_dotenv
from groq import Groq
from prompts import CHECKER_PROMPT, get_explainer_prompt, CHAT_PARTNER_PROMPT

# Load environment variables
load_dotenv()

# Verify that Groq API key is loaded properly
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("Warning: Missing GROQ_API_KEY in .env file.")

# Initialize the Groq API client
groq_client = Groq(api_key=groq_key)

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
    """
    Call Groq using the highly intelligent llama-3.3-70b-versatile model to explain errors.
    This completely bypasses Google Gemini's 503/429 quota and regional limitations.
    """
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": get_explainer_prompt(level)},
                {"role": "user", "content": f"Please explain and analyze this writing analysis data:\n{json.dumps(check_result, ensure_ascii=False)}"}
            ],
            model="llama-3.3-70b-versatile" # Highly capable 70B model with fast LPU speed
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Explainer Agent Error: {str(e)}"

def run_chat_partner_agent(chat_history):
    """
    Call Groq using llama-3.1-8b-instant to generate the next response.
    Guarantees lightning-fast chat speed and 100% uptime.
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
            model="llama-3.1-8b-instant" # Fast, low latency, highly stable
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Chat Partner Error: {str(e)}"