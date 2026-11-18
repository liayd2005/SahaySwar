import glob, json, os, re, wave
import numpy as np
import jiwer
import noisereduce as nr
from scipy.io import wavfile
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)
MODELS = {"hi": "models/vosk/vosk-model-small-hi-0.22", "en": "models/vosk/vosk-model-small-en-us-0.15"}
SNR_DB = 10
TMP = "data/tmp_denoise"
os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(0)


def clean(t):
    t = t.lower()
    t = re.sub(r"[।.,?!\"'()\-:;]", " ", t)
    return " ".join(t.split())


def clips(lang):
    for wav in sorted(glob.glob(f"data/bench/{lang}_*.wav")):
        with open(wav[:-4] + ".txt", encoding="utf-8") as f:
            yield wav, f.read()


def vosk_text(model, path):
    wf = wave.open(path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    while True:
        d = wf.readframes(4000)
        if not d:
            break
        rec.AcceptWaveform(d)
    return json.loads(rec.FinalResult()).get("text", "")


def save(x, sr, name):
    p = os.path.join(TMP, name)
    wavfile.write(p, sr, np.clip(x, -32768, 32767).astype(np.int16))
    return p


print("Vosk word error rate with noise added (SNR %d dB) and after noise cleanup\n" % SNR_DB)
print(f"{'lang':<5} {'clean':>8} {'noisy':>8} {'cleaned':>9}")
for lang, mpath in MODELS.items():
    model = Model(mpath)
    refs, h_clean, h_noisy, h_den = [], [], [], []
    for wav, ref in clips(lang):
        sr, x = wavfile.read(wav)
        if x.ndim > 1:
            x = x.mean(axis=1)
        x = x.astype(np.float32)
        p_sig = np.mean(x ** 2) + 1e-9
        noise = rng.normal(0, np.sqrt(p_sig / (10 ** (SNR_DB / 10))), size=x.shape)
        noisy = x + noise
        den = nr.reduce_noise(y=noisy, sr=sr, stationary=True)
        base = os.path.basename(wav)[:-4]
        refs.append(clean(ref))
        h_clean.append(clean(vosk_text(model, save(x, sr, base + "_c.wav"))))
        h_noisy.append(clean(vosk_text(model, save(noisy, sr, base + "_n.wav"))))
        h_den.append(clean(vosk_text(model, save(den, sr, base + "_d.wav"))))
    if refs:
        print(f"{lang:<5} {jiwer.wer(refs, h_clean):8.1%} {jiwer.wer(refs, h_noisy):8.1%} {jiwer.wer(refs, h_den):9.1%}")
    else:
        print(f"No clips for {lang}")