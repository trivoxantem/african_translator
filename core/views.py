# # core/views.py
# from django.shortcuts import render
# from .forms import TranslateForm
# from .utils import translate_text

# def home(request):
#     translation = None

#     if request.method == "POST":
#         form = TranslateForm(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             lang = form.cleaned_data['language']
#             translation = translate_text(text, lang)
#     else:
#         form = TranslateForm()

#     return render(request, "home.html", {
#         "form": form,
#         "translation": translation
#     })

from django.shortcuts import render
from .forms import TranslateForm, AudioUploadForm
from deep_translator import GoogleTranslator
import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

# Tiv dictionary
tiv_translations = {
    "hello": "m sugh u",
    "how are you?": "m ngoh?",
    "thank you": "mba yô",
    "good morning": "m sugh u u sha",
    "good night": "kaase",
    "what is your name?": "or u ken?"
}

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

def translate_to_tiv(text):
    return tiv_translations.get(text.lower().strip(), "Tiv translation not found.")

def translate(text, lang_name):
    if lang_name.lower() == "tiv":
        return translate_to_tiv(text)

    lang_code = supported_african_languages.get(lang_name)
    if not lang_code:
        return f"{lang_name} is not supported yet."

    try:
        return GoogleTranslator(source='en', target=lang_code).translate(text)
    except Exception as e:
        return f"Translation error: {e}"

def handle_audio_file(audio_file):
    recognizer = sr.Recognizer()
    file_ext = audio_file.name.split('.')[-1]
    temp_filename = f"temp_{uuid.uuid4()}.{file_ext}"
    with open(temp_filename, 'wb+') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    try:
        # Convert audio if not wav
        if file_ext != 'wav':
            sound = AudioSegment.from_file(temp_filename)
            wav_filename = f"{temp_filename}.wav"
            sound.export(wav_filename, format="wav")
        else:
            wav_filename = temp_filename

        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"[Error] {e}"
    finally:
        os.remove(temp_filename)
        if os.path.exists(wav_filename) and wav_filename != temp_filename:
            os.remove(wav_filename)

def translator_view(request):
    translation = None
    recognized_text = None

    if request.method == 'POST':
        form = TranslateForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('text', '')
            lang = form.cleaned_data['language']
            audio_file = form.cleaned_data.get('audio')

            if audio_file:
                recognized_text = handle_audio_file(audio_file)
                text = recognized_text if isinstance(recognized_text, str) else ""

            if text:
                translation = translate(text, lang)
    else:
        form = TranslateForm()

    return render(request, 'home.html', {
        'form': form,
        'translation': translation,
        'recognized_text': recognized_text
    })
