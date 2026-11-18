
from pathlib import Path
import re
import json

import pytesseract
import pymupdf
from PIL import Image

# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Project folders
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_text(pdf_path):
    """Extract text from PDF pages using OCR."""
    extracted_pages = []

    with pymupdf.open(pdf_path) as document:
        for page in document:
            # Convert each PDF page to an image
            pix = page.get_pixmap(dpi=300, alpha=False)
            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            # English OCR
            text = pytesseract.image_to_string(
                image,
                lang="eng+hin"
            )
            extracted_pages.append(text)

    return "\n".join(extracted_pages)


def split_questions(text):
    """Separate simply numbered questions."""
    questions = []
    current = None

    pattern = re.compile(
        r"^\s*(?:Q(?:uestion)?\.?\s*)?"
        r"(\d{1,2})\s*[.):]\s*(.*)$",
        re.IGNORECASE
    )

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Ignore the sample paper ending
        if "end of sample paper" in line.lower():
            continue

        match = pattern.match(line)

        if match:
            if current is not None:
                questions.append(current)

            current = {
                "number": int(match.group(1)),
                "text": match.group(2).strip()
            }

        elif current is not None:
            current["text"] += "\n" + line

    if current is not None:
        questions.append(current)

    return questions


def main():
    pdf_path = INPUT_DIR / "hindi_sample.pdf"

    if not pdf_path.exists():
        print("ERROR: sample.pdf was not found in the input folder.")
        print("Place your PDF inside the input folder and try again.")
        return

    print("Reading question paper...")
    text = extract_text(pdf_path)

    # Save all extracted text
    text_file = OUTPUT_DIR / "extracted_text.txt"
    text_file.write_text(text, encoding="utf-8")

    # Separate questions
    questions = split_questions(text)

    # Save questions in JSON format
    json_file = OUTPUT_DIR / "questions.json"
    json_file.write_text(
        json.dumps(
            {"language": "eng", "questions": questions},
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("\nExtraction completed.")
    print("Text file:", text_file)
    print("Questions file:", json_file)
    print("Questions detected:", len(questions))


if __name__ == "__main__":
    main()
