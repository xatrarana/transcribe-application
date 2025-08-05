# import whisper
# from googletrans import Translator
# import re


# model = whisper.load_model("medium", device="cpu")

# # Translate all speech into English (both Nepali & English parts)
# result = model.transcribe("minified.mp4", task="translate")
# english_text = result["text"]
# print("English transcript:\n", english_text)


# translator = Translator()
# nepali_translation = translator.translate(english_text, src='en', dest='ne').text

# print("\n✅ Final Nepali Transcript:\n", nepali_translation)


import whisper
import asyncio
from googletrans import Translator

async def main():
    # Load Whisper model on CPU
    model = whisper.load_model("medium", device="cpu")

    # Transcribe with translation task to English
    result = model.transcribe("minified.mp4", task="translate")
    english_text = result["text"]
    print("English transcript:\n", english_text)

    # Initialize async Translator
    translator = Translator()

    # Await the translate coroutine
    nepali_translation = await translator.translate(english_text, src='en', dest='ne')
    
    print("\n✅ Final Nepali Transcript:\n", nepali_translation.text)


if __name__ == "__main__":
    asyncio.run(main())
