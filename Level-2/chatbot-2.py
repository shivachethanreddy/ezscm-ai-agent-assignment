import os
import datetime
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from calculator_tool import calculator  # ✅ Calculator tool integration

# Load environment variables
load_dotenv()
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"❌ Error: Failed to configure Gemini API. {e}")
    exit()

# Gemini assistant setup
SYSTEM_INSTRUCTION = """
You are a helpful assistant. Always think step-by-step to answer a user's question.
Structure your output clearly with numbered steps or clear headings.

IMPORTANT: If the user asks for a direct mathematical calculation (e.g., '15 + 23' or 'what is 5 times 8'),
you MUST refuse. State that you are an explanatory AI, not a calculator, and suggest they use a calculator tool for accuracy.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction=SYSTEM_INSTRUCTION
)

def ask_gemini(user_question: str) -> str:
    try:
        response = model.generate_content(user_question)
        return re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())
    except Exception as e:
        return f"[Error] Could not get a response from Gemini. Details: {str(e)}"

# ✅ Detect symbolic or natural language math expressions

def is_math_expression(text: str) -> bool:
    math_keywords = ["add", "plus", "sum", "subtract", "minus", "difference",
                     "multiply", "times", "product", "divide", "divided", "+", "-", "*", "/"]
    return any(word in text.lower() for word in math_keywords)

# ✅ Convert natural language math to expression

def convert_natural_to_expression(text: str) -> str:
    text = text.lower().strip().replace("?", "")  # remove question mark

    if match := re.search(r"add\s+(\d+)\s+(?:and|to)\s+(\d+)", text):
        return f"{match.group(1)} + {match.group(2)}"
    if match := re.search(r"subtract\s+(\d+)\s+from\s+(\d+)", text):
        return f"{match.group(2)} - {match.group(1)}"
    if match := re.search(r"multiply\s+(\d+)\s+(?:and|by)\s+(\d+)", text):
        return f"{match.group(1)} * {match.group(2)}"
    if match := re.search(r"divide\s+(\d+)\s+by\s+(\d+)", text):
        return f"{match.group(1)} / {match.group(2)}"

    # ✅ Additional natural language patterns
    if match := re.search(r"what\s+is\s+(\d+)\s+(?:times|multiplied\s+by)\s+(\d+)", text):
        return f"{match.group(1)} * {match.group(2)}"
    if match := re.search(r"what\s+is\s+(\d+)\s+(?:divided\s+by)\s+(\d+)", text):
        return f"{match.group(1)} / {match.group(2)}"
    if match := re.search(r"what\s+is\s+(\d+)\s+(?:plus|added\s+to)\s+(\d+)", text):
        return f"{match.group(1)} + {match.group(2)}"
    if match := re.search(r"what\s+is\s+(\d+)\s+(?:minus|subtracted\s+from)\s+(\d+)", text):
        return f"{match.group(1)} - {match.group(2)}"

    return text  # fallback to raw if nothing matched
  # fallback to raw

# 🚫 Multi-intent detector

def is_mixed_intent(text: str) -> bool:
    text = text.lower()
    intent_splitters = [" and ", " also ", " while ", " as well as ", ", then "]
    if any(sep in text for sep in intent_splitters):
        has_math = is_math_expression(text)
        has_general = any(kw in text for kw in ["capital", "president", "country", "population", "who is"])
        return has_math and has_general
    return False

# 🧪 MAIN LOOP
def main():
    print("\U0001f9e0 Smart Assistant (Level 2 — Calculator Tool Enabled)\nType 'exit' or 'quit' to stop.")

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = f"logs/session_{timestamp}.json"
    session_log = []

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Assistant shutting down. Goodbye!")
            with open(log_path, "w") as f:
                json.dump(session_log, f, indent=2)
            print(f"📂 Session saved to {log_path}")
            break

        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_mixed_intent(user_input):
            answer = "I'm currently unable to handle multiple questions at once. Please ask one at a time."
            tools_used = []
            event = "multi_intent_detected"

        elif is_math_expression(user_input):
            try:
                expr = convert_natural_to_expression(user_input)
                result = calculator(expr)
                answer = f"The result is: {result}"
                tools_used = ["calculator"]
                event = "tool:calculator"
            except Exception as e:
                answer = f"[Error] Calculator tool failed: Invalid expression: {expr}. Error: {str(e)}"
                tools_used = ["calculator"]
                event = "error_occurred"

        else:
            answer = ask_gemini(user_input)
            tools_used = ["LLM (Gemini)"]
            if "calculator tool" in answer.lower():
                event = "math_refused"
            elif answer.startswith("[Error]"):
                event = "error_occurred"
            else:
                event = "query_answered"

        print(f"\nBot: {answer}")

        session_log.append({
            "timestamp": ts,
            "user_input": user_input,
            "bot_response": answer,
            "tools_used": tools_used,
            "event": event
        })

if __name__ == "__main__":
    main()

