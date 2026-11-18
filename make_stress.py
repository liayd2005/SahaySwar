import os
import sounddevice as sd
from scipy.io.wavfile import write

# Each item: (what to do, label saved in the .txt file)
CLIPS = {
    "hi": [
        ("say: अगला प्रश्न बहुत कठिन है", "अगला प्रश्न बहुत कठिन है"),
        ("say: पिछला प्रश्न मैंने हल कर लिया", "पिछला प्रश्न मैंने हल कर लिया"),
        ("say: कितना समय बचा है यह मुझे पता नहीं", "कितना समय बचा है यह मुझे पता नहीं"),
        ("say: प्रश्न दोहराओ शब्द का अर्थ क्या है", "प्रश्न दोहराओ शब्द का अर्थ क्या है"),
        ("say only: समय बचा है", "समय बचा है"),
        ("STAY SILENT for the whole clip", "[silence]"),
        ("make NOISE: cough, tap the desk, rustle paper", "[noise]"),
    ],
    "en": [
        ("say: the next question is about plants", "the next question is about plants"),
        ("say: the previous question was easy", "the previous question was easy"),
        ("say: how much time is left is not my concern", "how much time is left is not my concern"),
        ("say: please repeat the question in your answer", "please repeat the question in your answer"),
        ("say only: next", "next"),
        ("STAY SILENT for the whole clip", "[silence]"),
        ("make NOISE: cough, tap the desk, rustle paper", "[noise]"),
    ],
}

OUT = "data/stress"
os.makedirs(OUT, exist_ok=True)
sr = 16000
seconds = 6

for lang, items in CLIPS.items():
    for i, (instruction, label) in enumerate(items, 1):
        input(f"\n[{lang} {i}/{len(items)}] {instruction}\nPress Enter, wait half a second, then do it...")
        audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="int16")
        sd.wait()
        write(f"{OUT}/{lang}_{i:02d}.wav", sr, audio)
        with open(f"{OUT}/{lang}_{i:02d}.txt", "w", encoding="utf-8") as f:
            f.write(label)

print("Saved in", OUT)