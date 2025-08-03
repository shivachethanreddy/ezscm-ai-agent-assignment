import os
import datetime
import json
import re  # Used to clean markdown formatting like bold (**text**)
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (e.g., API keys) from .env file
load_dotenv()
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f" Error: Failed to configure Gemini API. {e}")
    exit()

# System-level instruction guiding the behavior of the Gemini assistant
SYSTEM_INSTRUCTION = """
You are a helpful assistant. Always think step-by-step to answer a user's question.
Structure your output clearly with numbered steps or clear headings.

IMPORTANT: If the user asks for a direct mathematical calculation (e.g., '15 + 23' or 'what is 5 times 8'),
you MUST refuse. State that you are an explanatory AI, not a calculator, and suggest they use a calculator tool for accuracy.
"""

# Initialize the Gemini model with custom system behavior
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction=SYSTEM_INSTRUCTION
)

# Send a question to the Gemini model and return a cleaned-up response
def ask_gemini(user_question: str) -> str:
    try:
        response = model.generate_content(user_question)
        # Remove bold markdown (e.g., **text**) from the response
        clean_text = re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())
        return clean_text
    except Exception as e:
        return f"[Error] Could not get a response from Gemini. Details: {str(e)}"

# Main interactive loop
def main():
    print(" Smart Assistant (Gemini Edition) — Type 'exit' or 'quit' to end.")

    # Create a directory to store logs if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create a unique filename for this session's log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_file_path = os.path.join(log_dir, f"session_{timestamp}.json")
    session_log = []

    # Chat loop begins
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print(" Assistant shutting down...")

            # Save the entire session's log to a JSON file
            with open(session_file_path, "w") as f:
                json.dump(session_log, f, indent=2)
            print(f" Session saved to {session_file_path}")
            break

        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if the user input looks like a math question
        math_keywords = ["+", "-", "*", "/", "add", "plus", "sum", "minus", "times", "multiply", "divide"]
        is_math = any(word in user_input.lower() for word in math_keywords)

        # Get the assistant's reply
        answer = ask_gemini(user_input)

        # Determine what kind of interaction this was
        if "calculator tool" in answer.lower():
            event = "math_refused"
        elif answer.startswith("[Error]"):
            event = "error_occurred"
        else:
            event = "query_answered"

        # Show the answer to the user
        print(f"\nBot: {answer}")

        # Log this interaction in memory
        session_log.append({
            "timestamp": ts,
            "user": user_input,
            "bot": answer,
            "tools_used": ["LLM (Gemini)"],
            "event": event
        })

# Entry point: runs the main loop
if __name__ == "__main__":
    main()
