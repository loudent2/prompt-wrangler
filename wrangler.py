# Makes a call to an ai to builda json output of medicaal devices based on a user propmpt. it Uses openrouter.ai
import requests
import json
import os
import time
import sys


API_KEY = os.getenv("OPENROUTER_API_KEY", "")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
# These value are hard coded for now but should be optional parameters
MODEL = "mistralai/mistral-7b-instruct"
TEMPERATURE = 0.3 
MAX_TOKENS = 512 

# This is the system prompt. It can be tweaked to change the behavior of the AI model.
SYSTEM_PROMPT = (
    "You are an expert assistant extracting structured JSON from medical equipment order notes.\n\n"
    "🧾 Rules:\n"
    "- Your output must be a flat JSON object.\n"
    "- DO NOT include fields with null values or empty arrays.\n"
    "- Only include fields if the input clearly mentions them.\n"
    "- The field 'device' is always required if a product is mentioned.\n\n"
    "📦 Field definitions:\n"
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


# Read user prompt
if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
else:
    user_prompt = input("📝 Paste the equipment order note:\n> ")


# Send request
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL,
    "temperature": TEMPERATURE,
    "max_tokens": MAX_TOKENS,
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt.strip()}
    ]
}

print("\n⏳ Processing...\n")
start = time.time()
response = requests.post(API_URL, headers=headers, json=data)
elapsed = time.time() - start

# Output
try:
    result = response.json()
    content = result['choices'][0]['message']['content']
    usage = result.get('usage', {})

    print("📤 JSON Output:\n")
    print(content)

    print("\n📊 Usage:")
    print(f"⏱️ Response Time: {elapsed:.2f}s")
    print(f"🔢 Prompt Tokens: {usage.get('prompt_tokens', 'N/A')}")
    print(f"🧠 Total Tokens: {usage.get('total_tokens', 'N/A')}")

except Exception as e:
    print("❌ Error:", e)
    print(response.text)
