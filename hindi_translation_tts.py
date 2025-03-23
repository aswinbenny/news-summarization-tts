from deep_translator import GoogleTranslator
from gtts import gTTS


def translate_to_hindi(text):
    """Translate English text to Hindi using Deep Translator."""
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)
    print("Translated Text:", translated_text)
    return translated_text


def text_to_speech_hindi(text):
    """Convert Hindi text to speech using gTTS."""
    tts = gTTS(text, lang="hi")
    audio_file = "output_hindi.mp3"
    tts.save(audio_file)
    return audio_file


def translate_and_speak(input_text):
    """Translate English text to Hindi and generate speech output."""
    hindi_text = translate_to_hindi(input_text)
    audio_file = text_to_speech_hindi(hindi_text)

    print("Audio file saved as:", audio_file)
    return hindi_text, audio_file