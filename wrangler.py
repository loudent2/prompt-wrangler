# Makes a call to an ai to builda json output of medicaal devices based on a user propmpt. it Uses openrouter.ai
import requests
import json
import os
import time
import sys
import argparse
import logging
import re

# Defaults and configuration
DEFAULT_MODEL = "mistralai/mistral-7b-instruct"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 512
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Load system prompt from file or use default
def load_system_prompt(path=None):
    if path:
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load system prompt from {path}: {e}")
            sys.exit(1)
    return (
        "You are an expert assistant extracting structured JSON from medical equipment order notes.\n\n"
        "\U0001F8FE Rules:\n"
        "- Your output must be a flat JSON object.\n"
        "- DO NOT include fields with null values or empty arrays.\n"
        "- Only include fields if the input clearly mentions them.\n"
        "- The field 'device' is always required if a product is mentioned.\n\n"
        "\U0001F4E6 Field definitions:\n"
        "- device: The main item being ordered (e.g., CPAP, oxygen concentrator, hospital bed).\n"
        "- type: An adjective describing the model (e.g., full face, lightweight).\n"
        "- features: An array of non-portable enhancements or accessories (e.g., trapeze bar, elevating leg rests).\n"
        "- components: An array of portable or attachable parts (e.g., portable, mouthpiece, humidifier).\n"
        "- diagnosis: A condition such as ALS, MS, COPD, Asthma, etc.\n"
        "- SpO2: If mentioned, include the value as a string with a percent sign (e.g., '87%').\n"
        "- qualifier: Clinical justification (e.g., AHI > 20, non-ambulatory).\n"
        "- usage: Array of use cases (e.g., 'sleep', 'exertion').\n"
        "- compliance_status: Only include if patient compliance is explicitly mentioned (e.g., 'compliant').\n"
        "- ordering_provider: The name of the doctor ordering the equipment.\n\n"
        "Do not infer values. Do not include fields if they are not present in the input."
    )

# Send request to AI
def call_ai(api_key, user_prompt, system_prompt, model, temperature, max_tokens):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt.strip()}
        ]
    }

    start = time.time()
    response = requests.post(API_URL, headers=headers, json=data)
    elapsed = time.time() - start

    try:
        result = response.json()
        content = result['choices'][0]['message']['content']
        usage = result.get('usage', {})

        return {
            "output": content,
            "elapsed": elapsed,
            "tokens": usage
        }
    except Exception as e:
        logger.error("Failed to parse response")
        logger.error(getattr(response, "text", "<no response text>"))
        raise


# Main CLI Entry Point
def main():
    parser = argparse.ArgumentParser(description="Send clinical note to LLM for structured output")
    parser.add_argument("note", nargs="?", help="Input clinical note or path to file (optional)")
    parser.add_argument("--system-prompt", help="Optional path to system prompt file")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--max_tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--api-key", help="API key or set OPENROUTER_API_KEY")

    args = parser.parse_args()

    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("API key missing. Provide via --api-key or OPENROUTER_API_KEY env var.")
        return 1

    user_prompt = None
    if args.note:
        if os.path.exists(args.note):
            with open(args.note, "r") as f:
                user_prompt = f.read()
        else:
            user_prompt = args.note
    elif not sys.stdin.isatty():
        logger.info("Reading input from stdin...")
        user_prompt = sys.stdin.read()
    else:
        user_prompt = input("📝 Paste the equipment order note:\n> ")

    user_prompt = re.sub(r"\s+", " ", user_prompt.strip())
    if len(user_prompt) < 10:
        logger.error("Input is too short or malformed.")
        return 1

    system_prompt = load_system_prompt(args.system_prompt)
    result = call_ai(api_key, user_prompt, system_prompt, args.model, args.temperature, args.max_tokens)

    print("\n📤 JSON Output:\n")
    print(result["output"])
    print("\n📊 Usage:")
    print(f"⏱️ Response Time: {result['elapsed']:.2f}s")
    print(f"🔢 Prompt Tokens: {result['tokens'].get('prompt_tokens', 'N/A')}")
    print(f"🧠 Total Tokens: {result['tokens'].get('total_tokens', 'N/A')}")

    return 0

if __name__ == "__main__":
    sys.exit(main())