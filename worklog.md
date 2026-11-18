# Work Log: Speech Module (SAHAY)

## 
- Installed Python 3.11.9, VS Code, created virtual environment.
- Installed edge-tts (first attempt failed with a network timeout; fixed by increasing the pip timeout and retries).
- Built baseline TTS for English (en-IN-NeerjaNeural) and Hindi (hi-IN-SwaraNeural).
- Tested 4 exam-style sentence types in each language: marks, options, math, long passage.

### Observation
- Hindi voice skipped the "=" symbol in math questions (read "5 15" instead of "5 equals 15").

### Fix
- Added a text normalization step (normalize.py) that converts symbols (=, +, %, etc.) into words in the chosen language before synthesis.

### Still to check
- Other symbols and formats (fractions, powers, units, chemical formulas).

## 
- Confirmed the normalization fix: Hindi voice now reads "=" as "बराबर है" after the symbol-to-word conversion.

## 
- The base Whisper model gave poor Hindi recognition, including hallucinated output in other languages; a larger model or a Hindi-specific model is needed.