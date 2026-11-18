import csv, glob, os, re, time
import numpy as np
import torch
import jiwer
from scipy.io import wavfile
from scipy.signal import resample_poly
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

MODELS = [
    ("wav2vec2-base-960h", "en", "facebook/wav2vec2-base-960h", 360),   # size is approximate
    ("wav2vec2-xlsr-hindi", "hi", "theainerd/Wav2Vec2-large-xlsr-hindi", 1200),  # size is approximate
]

summary, details = [], []


def clean(t):
    t = t.lower()
    t = re.sub(r"[।.,?!\"'()\-:;]", " ", t)
    return " ".join(t.split())


def clips(lang):
    for wav in sorted(glob.glob(f"data/bench/{lang}_*.wav")):
        with open(wav[:-4] + ".txt", encoding="utf-8") as f:
            yield wav, f.read()


def load_audio(path):
    sr, x = wavfile.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x.astype(np.float32)
    if np.abs(x).max() > 1.5:
        x = x / 32768.0
    if sr != 16000:
        x = resample_poly(x, 16000, sr).astype(np.float32)
    return x


for name, lang, repo, mb in MODELS:
    print(f"Loading {name} (first run downloads it, this can take a while)...")
    proc = Wav2Vec2Processor.from_pretrained(repo)
    try:
        model = Wav2Vec2ForCTC.from_pretrained(repo).eval()
    except Exception as e:
        print(f"Could not download {name}: {str(e)[:100]}")
        continue
    refs, hyps = [], []
    t0 = time.time()
    for wav, ref in clips(lang):
        x = load_audio(wav)
        inputs = proc(x, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            logits = model(inputs.input_values).logits
        hyp = clean(proc.batch_decode(torch.argmax(logits, dim=-1))[0])
        refs.append(clean(ref))
        hyps.append(hyp)
        details.append((name, lang, os.path.basename(wav), clean(ref), hyp))
        print(f"  {os.path.basename(wav)}: {hyp}")
    if refs:
        sec = (time.time() - t0) / len(refs)
        summary.append((name, lang, jiwer.wer(refs, hyps), sec, mb))
    else:
        print(f"No clips found for {lang}")

with open("data/wav2vec_summary.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "lang", "WER", "sec_per_clip", "size_MB"])
    for m, l, wer, s, mb in summary:
        w.writerow([m, l, f"{wer:.3f}", f"{s:.2f}", mb])

with open("data/wav2vec_details.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "lang", "clip", "reference", "heard"])
    w.writerows(details)

print("\nModel                 Lang   WER      Sec/clip   Size(MB)")
for m, l, wer, s, mb in summary:
    print(f"{m:<21} {l:<6} {wer:6.1%}   {s:7.2f}    {mb}")
print("\nSaved data/wav2vec_summary.csv and data/wav2vec_details.csv")