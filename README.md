# ezscm-ai-agent-assignment
This repository contains my solutions for the structured AI-focused assignment provided by ezSCM.ai, an AI-driven company specializing in intelligent supply chain management solutions.
# 🤖 Agentic AI Assistant (Internship @ ezSCM.ai)

**Author:** shivachetanreddy 
**Technologies:** Python, Gemini API (Google Generative AI), Tool-based Reasoning

---

## 📘 Project Summary

This project demonstrates an intelligent assistant that evolves across **three levels** of capability:

- ✅ Level 1: Gemini-based LLM chatbot
- ✅ Level 2: Calculator tool integration
- ✅ Level 3: Full agentic reasoning with multiple tools, multi-step queries, and memory

Each level includes logging, tool invocation tracking, and natural language handling.

---

## 📂 Project Structure

```plaintext
.
├── level1/
│   └── chatbot-1.py
│   └── logs/
├── level2/
│   └── chatbot-2.py
│   └── calculator_tool.py
│   └── logs/
├── level3/
│   └── full_agent.py
│   └── calculator_tool.py
│   └── translator_tool.py
│   └── logs_level3/
├── .env
└── README.md  ← You are here!
```

---

## 🔢 Level Breakdown

### ✅ Level 1 — Gemini LLM Only

- **File:** `chatbot-1.py`

#### 🔧 Functionality:
- Handles factual questions and explanations.
- Rejects direct math operations.

#### 💬 Example:
```
You: What is the capital of France?
Bot: The capital of France is Paris.
```

- **Logs:** Saved per session in `logs/`.

---

### ✅ Level 2 — Calculator Tool Integration

- **Files:** `chatbot-2.py`, `calculator_tool.py`

#### 🔧 Functionality:
- Detects and computes math queries using a custom calculator tool.
- Blocks multi-intent queries (e.g., "What is 2+2 and who is the PM?").

#### 💬 Example:
```
You: What is 12 plus 8?
Bot: The result is: 20
```

#### 🧮 Calculator Features:
- Supports: `+`, `-`, `*`, `/`
- Converts natural language math to expressions

- **Logs:** Saved in `logs/` with tools used and timestamps.

---

### ✅ Level 3 — Full Agentic AI

- **Files:** `full_agent.py`, `calculator_tool.py`, `translator_tool.py`

#### 🔧 Functionality:
- Multi-step reasoning and execution
- Combines:
  - Calculator tool
  - Translator tool (English → German)
  - Gemini LLM for factual questions/fallback

#### 💬 Example:
```
You: Translate 'Sunshine' into German and multiply 3 and 3.
Bot:
  Translated: Sonnenschein
  Multiply Result: 9
```

#### 🧠 Tool Routing:
- `calculator_tool.py` → Math queries
- `translator_tool.py` → Language translation
- Gemini API → General knowledge (e.g., capital of Italy)

- **Logs:** Each interaction saved in `logs_level3/` with steps, tools, and response.

---

## 📝 Setup Instructions

1. Clone the project:
   ```bash
   git clone https://github.com/shivachethanreddy/ezscm-ai-agent-assignment.git
   cd agentic-ai-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Google API key to a `.env` file:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   ```

4. Run the desired level:
   ```bash
   python chatbot-1.py        # Level 1
   python chatbot-2.py        # Level 2
   python full_agent.py       # Level 3
   ```

---

## ✅ Deliverables Summary

| Level   | Files                                              | Log Directory     |
|---------|----------------------------------------------------|-------------------|
| Level 1 | `chatbot-1.py`                                     | `logs/`           |
| Level 2 | `chatbot-2.py`, `calculator_tool.py`               | `logs/`           |
| Level 3 | `full_agent.py`, `calculator_tool.py`, `translator_tool.py` | `logs_level3/` |

---

## 📌 Project Notes

- Built with **Gemini 1.5 Flash API**.
- Designed with **agentic reasoning** principles.
- Tool calls, intermediate steps, and timestamps are **fully logged**.
- All levels support local testing without front-end.

---

✅ All use cases passed.  
🧠 Agentic logic, multi-tool reasoning, and fallback handling complete.
