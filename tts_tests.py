from tts import speak

TESTS = [
    ("en", "q1_marks", "Question 3. Explain Newton's second law. (5 marks)"),
    ("en", "q2_options", "Which of the following is correct? Option A, 25 percent. Option B, 3.5 kilograms. Option C, none of these."),
    ("en", "q3_math", "Solve for x: 2x + 5 = 15. Then find the value of x squared."),
    ("en", "q4_long", "Read the following passage carefully and answer the questions that follow. The Industrial Revolution began in Britain in the eighteenth century and transformed the way goods were produced, bringing major changes to society, economy and daily life."),
    ("hi", "q1_marks", "प्रश्न 3. न्यूटन का दूसरा नियम समझाइए। (5 अंक)"),
    ("hi", "q2_options", "निम्नलिखित में से कौन सा सही है? विकल्प A, 25 प्रतिशत। विकल्प B, 3.5 किलोग्राम। विकल्प C, इनमें से कोई नहीं।"),
    ("hi", "q3_math", "x का मान ज्ञात कीजिए: 2x + 5 = 15। फिर x का वर्ग निकालिए।"),
    ("hi", "q4_long", "निम्नलिखित गद्यांश को ध्यानपूर्वक पढ़िए और उसके बाद आने वाले प्रश्नों के उत्तर दीजिए। औद्योगिक क्रांति अठारहवीं शताब्दी में ब्रिटेन में शुरू हुई और उसने वस्तुओं के उत्पादन का तरीका बदल दिया।"),
]

for lang, name, text in TESTS:
    path = f"data/{lang}_{name}.mp3"
    speak(text, lang, path)
    print("Saved", path)

print("All done.")