import glob, json, os, wave
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)
SLACK = 1  # extra words allowed in the unrestricted transcript

COMMANDS = {
    "hi": ["प्रश्न दोहराओ", "कितना समय बचा है", "अगला प्रश्न", "पिछला प्रश्न"],
    "en": ["repeat the question", "how much time is left",
           "next question", "previous question"],
}
MODELS = {
    "hi": "models/vosk-model-small-hi-0.22",
    "en": "models/vosk-model-small-en-us-0.15",
}


def run(model, path, phrases=None):
    wf = wave.open(path, "rb")
    if phrases:
        grammar = json.dumps(phrases + ["[unk]"], ensure_ascii=False)
        rec = KaldiRecognizer(model, wf.getframerate(), grammar)
    else:
        rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        rec.AcceptWaveform(data)
    return json.loads(rec.FinalResult()).get("text", "").strip()


for lang in ["hi", "en"]:
    model = Model(MODELS[lang])
    cmds = COMMANDS[lang]
    missed = false_acc = n_cmd = n_other = 0
    print(f"\n=== {lang} ===")
    for folder in ["data/bench", "data/stress"]:
        for wav in sorted(glob.glob(f"{folder}/{lang}_*.wav")):
            with open(wav[:-4] + ".txt", encoding="utf-8") as f:
                ref = f.read().strip()
            restricted = run(model, wav, cmds)
            free = run(model, wav)
            accepted = (restricted in cmds and
                        len(free.split()) <= len(restricted.split()) + SLACK)
            is_cmd = ref in cmds
            if is_cmd:
                n_cmd += 1
                missed += not accepted
                verdict = "ACCEPTED (correct)" if accepted else "MISSED"
            else:
                n_other += 1
                false_acc += accepted
                verdict = "FALSE ACCEPT" if accepted else "rejected (correct)"
            print(f"{folder[5:]}/{os.path.basename(wav)}  said: {ref!r}")
            print(f"     restricted: {restricted!r}   free: {free!r}   -> {verdict}")
    print(f"Commands missed: {missed}/{n_cmd}")
    print(f"Non-commands wrongly accepted: {false_acc}/{n_other}")