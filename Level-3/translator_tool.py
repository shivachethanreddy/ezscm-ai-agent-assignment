
def translate_to_german(text: str) -> str:
    translations = {
        "Good Morning": "Guten Morgen",
        "Have a nice day": "Einen schönen Tag noch",
        "Sunshine": "Sonnenschein"
    }
    return translations.get(text.strip(), f"[No translation found for '{text}']")
