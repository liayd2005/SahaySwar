import csv, glob, json, os, re, time, wave
import jiwer
from faster_whisper import WhisperModel
from vosk import Model as VoskModel, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)

WHISPER_SIZES = {"base": 140, "small": 460}  # approx. size on disk in MB
VOSK_PATHS = {
    "hi": "models/vosk-model-small-hi-0.22",
    "en": "models/vosk-model-small-en-us-0.15",
}

summary, details = [], []


def clean(t):
    t = t.lower()
    t = re.sub(r"[।.,?!\"'()\-:;]", " ", t)
    return " ".join(t.split())


def folder_mb(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return round(total / 1e6)


def vosk_transcribe(model, path):
    wf = wave.open(path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        rec.AcceptWaveform(data)
    return json.loads(rec.FinalResult()).get("text", "")


def clips(lang):
    for wav in sorted(glob.glob(f"data/bench/{lang}_*.wav")):
        with open(wav[:-4] + ".txt", encoding="utf-8") as f:
            yield wav, f.read()


def run(name, lang, size_mb, transcribe):
    refs, hyps = [], []
    t0 = time.time()
    for wav, ref in clips(lang):
        hyp = clean(transcribe(wav))
        refs.append(clean(ref))
        hyps.append(hyp)
        details.append((name, lang, os.path.basename(wav), clean(ref), hyp))
    if not refs:
        print(f"No clips found for {lang}")
        return
    sec = (time.time() - t0) / len(refs)
    summary.append((name, lang, jiwer.wer(refs, hyps), sec, size_mb))


for size, mb in WHISPER_SIZES.items():
    print(f"Loading whisper {size} (first run downloads it)...")
    wm = WhisperModel(size, device="cpu", compute_type="int8")
    for lang in ["hi", "en"]:
        def tr(path, wm=wm, lang=lang):
            segs, _ = wm.transcribe(path, language=lang, beam_size=5,
                                    vad_filter=True,
                                    condition_on_previous_text=False,
                                    temperature=0.0)
            return " ".join(s.text for s in segs)
        print(f"  testing {lang}...")
        run(f"whisper-{size}", lang, mb, tr)

for lang, path in VOSK_PATHS.items():
    if not os.path.isdir(path):
        print(f"Skipping Vosk {lang}: {path} not found")
        continue
    vm = VoskModel(path)
    print(f"Testing vosk {lang}...")
    run("vosk-small", lang, folder_mb(path),
        lambda p, vm=vm: vosk_transcribe(vm, p))

with open("data/bench_summary.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "lang", "WER", "sec_per_clip", "size_MB"])
    for m, l, wer, s, mb in summary:
        w.writerow([m, l, f"{wer:.3f}", f"{s:.2f}", mb])

with open("data/bench_details.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "lang", "clip", "reference", "heard"])
    w.writerows(details)

print("\nModel            Lang   WER      Sec/clip   Size(MB)")
for m, l, wer, s, mb in summary:
    print(f"{m:<16} {l:<6} {wer:6.1%}   {s:7.2f}    {mb}")
print("\nSaved data/bench_summary.csv and data/bench_details.csv")