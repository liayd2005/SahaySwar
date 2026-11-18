import io
import os

CHECKS = {
    "models/vosk-model-small-hi-0.22":
        "प्रश्न दोहराओ कितना समय बचा है अगला पिछला",
    "models/vosk-model-small-en-us-0.15":
        "repeat the question how much time is left next previous",
}

for folder, words in CHECKS.items():
    path = None
    for root, _, files in os.walk(folder):
        if "words.txt" in files:
            path = os.path.join(root, "words.txt")
            break
    print("\n", folder)
    if not path:
        print("  no words.txt found in this model")
        continue
    with io.open(path, encoding="utf-8") as f:
        vocab = {line.split()[0] for line in f if line.strip()}
    for w in words.split():
        print(f"  {w:12s}", "OK" if w in vocab else "MISSING")