import re

SYMBOLS = {
    "en": {
        "=": " equals ",
        "+": " plus ",
        "×": " times ",
        "÷": " divided by ",
        "%": " percent",
    },
    "hi": {
        "=": " बराबर है ",
        "+": " जमा ",
        "×": " गुणा ",
        "÷": " भाग ",
        "%": " प्रतिशत",
    },
}

MINUS = {"en": " minus ", "hi": " ऋण "}


def normalize(text, lang):
    # a dash with spaces on both sides, or between two digits, is a minus sign
    text = re.sub(r"(?<=\d)\s*-\s*(?=\d)", MINUS[lang], text)
    text = re.sub(r"\s-\s", MINUS[lang], text)
    for symbol, word in SYMBOLS[lang].items():
        text = text.replace(symbol, word)
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    print(normalize("x का मान ज्ञात कीजिए: 2x + 5 = 15।", "hi"))
    print(normalize("Solve for x: 2x + 5 = 15. Then 25% of 10 - 3.", "en"))