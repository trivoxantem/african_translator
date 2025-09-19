# core/utils.py
from deep_translator import GoogleTranslator

supported_african_languages = {
    "Yoruba": "yo",
    "Igbo": "ig",
    "Hausa": "ha",
    "Swahili": "sw",
    "Zulu": "zu",
    "Xhosa": "xh",
    "Somali": "so",
    "Amharic": "am",
    "Arabic": "ar",
    "Afrikaans": "af",
    "Tigrinya": "ti"
}

tiv_translations = {
    "hello": "m sugh u",
    "how are you?": "m ngoh?",
    "thank you": "mba yô",
    "good morning": "m sugh u u sha",
    "good night": "kaase",
    "what is your name?": "or u ken?"
}

def translate_text(text, language_name):
    text = text.lower().strip()
    if language_name.lower() == "tiv":
        return tiv_translations.get(text, "Tiv translation not found.")

    lang_code = supported_african_languages.get(language_name)
    if not lang_code:
        return f"{language_name} is not supported."

    try:
        return GoogleTranslator(source='en', target=lang_code).translate(text)
    except Exception as e:
        return f"Error: {e}"
