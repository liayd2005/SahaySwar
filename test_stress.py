import glob, json, os, wave
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)

COMMANDS = {
    "hi": ["प्रश्न दोहराओ", "कितना समय बचा है", "अगला प्रश्न", "पिछला प्रश्न"],
    "en": ["repeat the question", "how much time is left",
           "next question", "previous question"],
}
MODELS = {
    "hi": "models/vosk-model-small-hi-0.22",
    "en": "models/vosk-model-small-en-us-0.15",
}


def recognize(model, phrases, path):
    wf = wave.open(path, "rb")
    grammar = json.dumps(phrases + ["[unk]"], ensure_ascii=False)
    rec = KaldiRecognizer(model, wf.getframerate(), grammar)
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        rec.AcceptWaveform(data)
    return json.loads(rec.FinalResult()).get("text", "").strip()


for lang in ["hi", "en"]:
    model = Model(MODELS[lang])
    cmds = COMMANDS[lang]
    false_acc = total = 0
    print(f"\n=== {lang} ===")
    for wav in sorted(glob.glob(f"data/stress/{lang}_*.wav")):
        with open(wav[:-4] + ".txt", encoding="utf-8") as f:
            ref = f.read().strip()
        heard = recognize(model, cmds, wav)
        total += 1
        bad = heard in cmds
        false_acc += bad
        mixed = (not bad) and any(c.split()[0] in heard for c in cmds)
        flag = "FALSE ACCEPT" if bad else ("partial command words" if mixed else "ok")
        print(f"{os.path.basename(wav)}  said: {ref!r}  heard: {heard!r}  {flag}")
    print(f"Wrongly accepted as a command: {false_acc}/{total}")