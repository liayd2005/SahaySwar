import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

print("Loading speech model (the first run downloads it)...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Model loaded.")


def record(seconds=5, path="data/input.wav", sr=16000):
    print(f"Speak now for {seconds} seconds...")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="int16")
    sd.wait()
    write(path, sr, audio)
    print("Recording finished.")
    return path


def listen(path, lang):
    segments, _ = model.transcribe(path, language=lang)
    return " ".join(s.text for s in segments).strip()


if __name__ == "__main__":
    lang = input("Language (en or hi): ").strip()
    p = record(5)
    print("You said:", listen(p, lang))