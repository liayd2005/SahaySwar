import os, subprocess, sys, time
from normalize import normalize

VOICES = ["priyamvada", "pratham", "rohan"]
TESTS = [
    ("q1_marks", "प्रश्न 3. न्यूटन का दूसरा नियम समझाइए। (5 अंक)"),
    ("q2_options", "निम्नलिखित में से कौन सा सही है? विकल्प A, 25 प्रतिशत। विकल्प B, 3.5 किलोग्राम। विकल्प C, इनमें से कोई नहीं।"),
    ("q3_math", "x का मान ज्ञात कीजिए: 2x + 5 = 15। फिर x का वर्ग निकालिए।"),
    ("q4_long", "निम्नलिखित गद्यांश को ध्यानपूर्वक पढ़िए और उसके बाद आने वाले प्रश्नों के उत्तर दीजिए। औद्योगिक क्रांति अठारहवीं शताब्दी में ब्रिटेन में शुरू हुई और उसने वस्तुओं के उत्पादन का तरीका बदल दिया।"),
]

env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
os.makedirs("data/piper", exist_ok=True)

for v in VOICES:
    model = f"models/piper/hi_IN-{v}-medium.onnx"
    if not os.path.exists(model):
        print("MISSING", model)
        continue
    print(f"\n{v}: {round(os.path.getsize(model) / 1e6)} MB")
    for name, text in TESTS:
        out = f"data/piper/hi_{v}_{name}.wav"
        t0 = time.time()
        r = subprocess.run(
            [sys.executable, "-m", "piper", "-m", model, "-f", out],
            input=normalize(text, "hi").encode("utf-8"),
            capture_output=True, env=env,
        )
        if r.returncode != 0:
            print(f"  FAILED {name}: {r.stderr.decode(errors='replace')[-200:]}")
        else:
            print(f"  {name}: {time.time() - t0:.1f} s")