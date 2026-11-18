import os
import sounddevice as sd
from scipy.io.wavfile import write

SENTENCES = {
    "hi": [
        "भारत का राष्ट्रीय पशु कौन सा है",
        "न्यूटन का दूसरा नियम समझाइए",
        "भारत की राजधानी का नाम बताइए",
        "जल का रासायनिक सूत्र लिखिए",
        "पौधे अपना भोजन कैसे बनाते हैं",
        "मुगल साम्राज्य की स्थापना किसने की",
        "प्रश्न दोहराओ",
        "कितना समय बचा है",
        "अगला प्रश्न",
        "पिछला प्रश्न",
    ],
    "en": [
        "which is the national animal of india",
        "explain newton's second law of motion",
        "name the capital of india",
        "write the chemical formula of water",
        "how do plants make their food",
        "who founded the mughal empire",
        "repeat the question",
        "how much time is left",
        "next question",
        "previous question",
    ],
}

os.makedirs("data/bench", exist_ok=True)
sr = 16000
seconds = 6

for lang, lines in SENTENCES.items():
    for i, text in enumerate(lines, 1):
        input(f"\n[{lang} {i}/{len(lines)}] Press Enter, then say:  {text}")
        audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="int16")
        sd.wait()
        write(f"data/bench/{lang}_{i:02d}.wav", sr, audio)
        with open(f"data/bench/{lang}_{i:02d}.txt", "w", encoding="utf-8") as f:
            f.write(text)

print("Dataset saved in data/bench")