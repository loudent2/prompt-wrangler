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

### ✅ 2. Install Dependencies

## ✅ Recommended Fix: Use a Virtual Environmeny
Install the required Python package: 
🛠️ Create a Virtual Environment
```bash
python3 -m venv venv
```
⚡ Activate the Virtual Environment
```bash
source venv/bin/activate
```
Install reqests

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

You can run the tool by passing input directly:

```bash
python wrangler.py "Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron."
```

Or run it interactively:

```bash
python wrangler.py
# Then paste the input when prompted
```

---

## ⚙️ Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🧾 Flat JSON Output       | No nesting. Only includes fields explicitly mentioned in the input.         |
| 🤖 OpenRouter LLM API     | Uses models like `mistral-7b-instruct` via OpenRouter.                      |
| 🔍 Rule-Based Extraction  | Applies logic for when to use `components` vs `features`.                   |
| ⏱️ Metrics Reporting      | Shows total tokens and response time.                                       |
| 🛠️ Input Flexibility      | Accepts CLI arguments or prompts interactively.                             |

---

## 🧱 Design Philosophy

- **Single Responsibility**: One input, one purpose — transform unstructured clinical text into useful structured output.
- **No Manual Tagging**: The LLM infers everything from free text.
- **Flat Schema**: Keeps the output clean and easy to work with downstream (e.g., storing in DynamoDB, piping into ETL).
- **Selective Output**: Fields like `"SpO2"` or `"compliance_status"` are only included if explicitly mentioned — no nulls.
- **Domain Awareness**: Prompt encourages correct placement of adjectives (e.g. “portable” → `components`, “elevating leg rests” → `features`).

---

## 🔬 How It Works

### 🧠 Prompt
The script sends a fixed system prompt that instructs the LLM how to extract and label clinical data. The prompt includes:
- Explicit field definitions
- A rule: *no nulls, only include mentioned fields*
- Adjective handling rules for `features` vs `components`

### 📤 OpenRouter API Call
The script uses `requests.post()` to send a chat-style prompt to the LLM endpoint, and measures response time + token usage.

---

## ✅ Example Inputs

Try these:

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

## 🧪 Tests (Optional Extension)

Tests can be added using `unittest` and mocking `requests.post` to simulate LLM responses. For now, the script is kept minimal to focus on core functionality.

---

## 👨‍⚕️ Built For

- AI engineers tuning prompts for healthcare workflows
- DME teams needing lightweight tooling for document parsing
- Developers integrating LLM-based preprocessing into pipelines

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
