# 🧠 Prompt Wrangler: Clinical Note Extractor

A fast, minimalist **CLI tool** for extracting structured JSON from messy medical equipment order notes using an LLM via **OpenRouter**.

Built as part of a 1-hour LLM tuning challenge. Focused on clarity, usefulness, and rule-based extraction for DME (Durable Medical Equipment) use cases.

---

## 🚀 What It Does

Given input like:

```
Patient diagnosed with COPD, SpO2 measured at 87% on room air. Needs portable oxygen concentrator for use during exertion and sleep. Dr. Chase signed the order.
```

It extracts structured data like:

```json
{
  "device": "oxygen concentrator",
  "components": ["portable"],
  "diagnosis": "COPD",
  "SpO2": "87%",
  "usage": ["exertion", "sleep"],
  "ordering_provider": "Dr. Chase"
}
```

The tool automatically:
- Identifies key clinical terms (diagnosis, qualifiers, usage context)
- Classifies descriptors as `features` or `components`
- Omits fields not explicitly present
- Returns flat JSON (no nested objects)
- Displays token usage + response time

---

## 🛠️ Install Prerequisites

### ✅ 1. Python 3.8+
Ensure you have Python installed:

```bash
python3 --version
```

If not installed, use Homebrew (macOS):
```bash
brew install python
```

---

### ✅ 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

Then install the dependency:

```bash
pip install requests
```

---

### ✅ 3. Get an OpenRouter API Key

- Sign up at [https://openrouter.ai](https://openrouter.ai)
- Copy your API key
- Set it in your terminal:

```bash
export OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 How to Run

### Run from CLI with direct input:

```bash
python wrangler.py "Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron."
```

# OR from a file:
```bash
python wrangler.py notes/sample.txt
```

# OR via stdin:
```bash
cat notes/sample.txt | python wrangler.py
```
# OR interactively (no arguments):
python wrangler.py
### Run with arguments (optional):

```bash
python wrangler.py notes/sample.txt --system-prompt prompts/default.txt --temperature 0.4 --model mistralai/mistral-7b-instruct
```

---

## ⚙️ Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🧾 Flat JSON Output       | No nesting. Only includes fields explicitly mentioned in the input.         |
| 🤖 OpenRouter LLM API     | Uses models like `mistral-7b-instruct` via OpenRouter.                      |
| 🔍 Rule-Based Extraction  | Applies logic for when to use `components` vs `features`.                   |
| ⏱️ Metrics Reporting      | Shows total tokens and response time.                                       |
| 🛠️ Input Flexibility      | Accepts multi-line input via file, stdin, or interactive prompt.            |

---

## 🧱 Design Philosophy

- **Single Responsibility**: One input, one purpose — transform unstructured clinical text into useful structured output.
- **No Manual Tagging**: The LLM infers everything from free text.
- **Flat Schema**: Keeps the output clean and easy to work with downstream (e.g., storing in DynamoDB, piping into ETL).
- **Selective Output**: Fields like `"SpO2"` or `"compliance_status"` are only included if explicitly mentioned — no nulls.
- **Domain Awareness**: Prompt encourages correct placement of adjectives (e.g. “portable” → `components`, “elevating leg rests” → `features`).
- **Input Sanitation**: Trims whitespace, normalizes spacing, validates minimum input length

---

## 🔬 How It Works

### 🧠 Prompt
The script sends a default or user-specified system prompt to guide the LLM. Prompts can be swapped using `--system-prompt prompts/strict_json.txt`.

### 📤 OpenRouter API Call
Uses `requests.post()` to submit the chat request and logs timing + token metrics.

---

## ✅ Example Inputs

```bash
python wrangler.py "Patient has MS with significant mobility issues. Recommended a lightweight manual wheelchair with elevating leg rests. Ordered by Dr. Taub."
```

```bash
python wrangler.py "Asthma diagnosis confirmed. Prescribing nebulizer with mouthpiece and tubing. Dr. Foreman completed the documentation."
```

---

## ✅ Example Output

```json
{
  "device": "nebulizer",
  "components": ["mouthpiece", "tubing"],
  "diagnosis": "Asthma",
  "ordering_provider": "Dr. Foreman"
}
```

---

## ✅ Tests

Run unit tests (mocked LLM responses) with:

```bash
python -m unittest discover tests/
```

---

## 🧠 With More Time...

- Add session history or run saving
- Build a Streamlit-based prompt playground
- Implement schema validation or error correction
- Add a “How to improve this prompt” LLM feedback feature

---

## 👨‍⚕️ Built For

- AI engineers tuning prompts for healthcare workflows
- DME teams needing lightweight tooling for document parsing
- Developers integrating LLM-based preprocessing into pipelines