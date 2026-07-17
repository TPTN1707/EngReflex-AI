import json
from groq import Groq
from src.config import Config
from src.prompts.checker import CHECKER_PROMPT
from src.prompts.explainer import get_explainer_prompt
# Import the new dynamic prompt and greeting helpers
from src.prompts.chat_partner import get_chat_partner_prompt

# Validate configuration before initializing clients
Config.validate_config()

# Initialize the centralized Groq client
groq_client = Groq(api_key=Config.GROQ_API_KEY)

def run_checker_agent(text_input):
    """Call Groq to perform rapid grammar and Viet-lish checks using llama-3.3-70b"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": CHECKER_PROMPT},
                {"role": "user", "content": text_input}
            ],
            model=Config.CHECKER_MODEL, 
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": f"Checker Agent Error: {str(e)}"}

def run_explainer_agent(check_result, level="vietnamese"):
    """Call Groq using the larger model to explain detected errors"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": get_explainer_prompt(level)},
                {"role": "user", "content": f"Please explain and analyze this writing analysis data:\n{json.dumps(check_result, ensure_ascii=False)}"}
            ],
            model=Config.EXPLAINER_MODEL
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Explainer Agent Error: {str(e)}"

# Updated to accept scenario argument dynamically
def run_chat_partner_agent(chat_history, scenario="casual"):
    """
    Call Groq using llama-3.1-8b-instant to generate natural conversational responses.
    Dynamically loads the correct system instructions based on the selected writing scenario.
    """
    try:
        # Load the dynamic scenario prompt
        messages = [{"role": "system", "content": get_chat_partner_prompt(scenario)}]
        for msg in chat_history:
            role = "assistant" if msg["role"] == "model" else "user"
            text = msg["parts"][0]["text"]
            messages.append({"role": role, "content": text})

        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model=Config.CHAT_PARTNER_MODEL
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Chat Partner Error: {str(e)}"