import glob, json, re, time, wave
import jiwer
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)
MODELS = {
    "en-us": "models/vosk-model-small-en-us-0.15",
    "en-in": "models/vosk-model-small-en-in-0.4",
}


def clean(t):
    t = t.lower()
    t = re.sub(r"[।.,?!\"'()\-:;]", " ", t)
    return " ".join(t.split())


def transcribe(model, path):
    wf = wave.open(path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        rec.AcceptWaveform(data)
    return json.loads(rec.FinalResult()).get("text", "")


clips = sorted(glob.glob("data/bench/en_*.wav"))
refs = []
for w in clips:
    with open(w[:-4] + ".txt", encoding="utf-8") as f:
        refs.append(clean(f.read()))

for name, path in MODELS.items():
    m = Model(path)
    t0 = time.time()
    hyps = [clean(transcribe(m, w)) for w in clips]
    sec = (time.time() - t0) / len(clips)
    print(f"\n{name}: WER {jiwer.wer(refs, hyps):.1%}   {sec:.2f} s/clip")
    for r, h in zip(refs, hyps):
        print("   said:", r, "| heard:", h)