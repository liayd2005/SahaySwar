import asyncio
import edge_tts
from normalize import normalize

VOICES = {
    "en": "en-IN-NeerjaNeural",
    "hi": "hi-IN-SwaraNeural",
}


async def _synth(text, lang, path):
    await edge_tts.Communicate(text, VOICES[lang]).save(path)


def speak(text, lang, path="out.mp3"):
    text = normalize(text, lang)
    print("Speaking:", text)
    asyncio.run(_synth(text, lang, path))
    return path