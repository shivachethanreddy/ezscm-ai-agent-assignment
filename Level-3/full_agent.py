

import os
import datetime
import json
import re
from dotenv import load_dotenv
from calculator_tool1 import calculator
from translator_tool import translate_to_german
import google.generativeai as genai

# === Load Gemini API ===
load_dotenv()
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"❌ Failed to configure Gemini API: {e}")
    exit()

# === Gemini setup ===
SYSTEM_INSTRUCTION = """
You are a helpful assistant. Always think step-by-step to answer a user's question.
Use tools if needed (like translation or calculator).
"""
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction=SYSTEM_INSTRUCTION
)

def ask_gemini(query: str) -> str:
    try:
        response = model.generate_content(query)
        return re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())
    except Exception as e:
        return f"[Error] Gemini failed: {str(e)}"

# === Logging ===
def log_interaction(data, log_dir="logs_level3"):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"log_{timestamp}.json")
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

# === Natural Language Math → List of Expressions ===
def convert_all_math_expressions(text: str) -> list:
    text = text.lower().strip().replace("?", "")
    expressions = []

    # Match: add 2 and 2
    for match in re.finditer(r"add\s+(\d+)\s+(?:and|to)\s+(\d+)", text):
        expressions.append(("add", f"{match.group(1)} + {match.group(2)}"))

    # Match: multiply 3 and 3
    for match in re.finditer(r"multiply\s+(\d+)\s+(?:and|by)?\s*(\d+)", text):
        expressions.append(("multiply", f"{match.group(1)} * {match.group(2)}"))

    # Match: what is 5 times 6
    for match in re.finditer(r"what\s+is\s+(\d+)\s+(?:times|multiplied\s+by)\s+(\d+)", text):
        expressions.append(("multiply", f"{match.group(1)} * {match.group(2)}"))

    # Match: what is 4 plus 3
    for match in re.finditer(r"what\s+is\s+(\d+)\s+(?:plus|added\s+to)\s+(\d+)", text):
        expressions.append(("add", f"{match.group(1)} + {match.group(2)}"))

    return expressions

# === Main Agent ===
def handle_query(query: str) -> str:
    steps = []
    tools_used = []
    responses = []
    query_lower = query.lower()

    # === 1. Handle Translation ===
    if "translate" in query_lower:
        match = re.search(r"translate\s+['\"]?([^'\"]+)['\"]?\s+into\s+german", query, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            translated = translate_to_german(text)
            steps.append({"action": "translate", "input": text, "output": translated})
            tools_used.append("translator")
            responses.append(f"Translated: {translated}")

    # === 2. Handle Multiple Calculator Ops ===
    if any(kw in query_lower for kw in ["add", "plus", "sum", "multiply", "times", "*", "+"]):
        try:
            expressions = convert_all_math_expressions(query)
            if not expressions:
                raise ValueError("No valid math expressions found.")

            for operation, expr in expressions:
                result = calculator(expr)
                steps.append({"action": operation, "input": expr, "output": result})
                tools_used.append("calculator")
                responses.append(f"{operation.title()} Result: {result}")

        except Exception as e:
            responses.append(f"[Error] Calculator failed: {e}")
            tools_used.append("calculator")

    # === 3. Handle Factual Queries ===
    if "capital of italy" in query_lower or "distance between earth and mars" in query_lower:
        fact_response = ask_gemini(query)
        steps.append({"action": "knowledge", "input": query, "output": fact_response})
        tools_used.append("LLM (Gemini)")
        responses.append(fact_response)

    # === 4. Fallback LLM if nothing else matched ===
    if not responses:
        fallback = ask_gemini(query)
        steps.append({"action": "llm_fallback", "input": query, "output": fallback})
        tools_used.append("LLM (Gemini)")
        responses.append(fallback)

    # === Logging ===
    final_response = "\n".join(responses)
    log_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "steps": steps,
        "tools_used": list(set(tools_used)),
        "response": final_response
    }
    log_interaction(log_data)
    return final_response

# === Entry Point ===
if __name__ == "__main__":
    print(" Full Agent (Level 3) Ready — Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = handle_query(user_input)
        print(f"\nBot: {response}")
