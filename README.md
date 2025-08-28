Nice choice 👍 — **Coqui TTS** is much easier to set up than Tacotron2 + WaveGlow, and it already comes with many **pretrained TTS models**.

Here’s how you can install it on **Ubuntu** and generate speech:

---

## 🔹 1. Install Dependencies

First update packages:

```bash
sudo apt update
sudo apt install python3-pip git ffmpeg espeak -y
pip install --upgrade pip
```

> ⚠️ `ffmpeg` and `espeak` are required for audio handling.

---

## 🔹 2. Install Coqui TTS

You can install directly from PyPI:

```bash
pip install TTS
```

If you want the latest development version:

```bash
pip install git+https://github.com/coqui-ai/TTS
```

---

## 🔹 3. Run a Pre-trained TTS Model

Coqui provides dozens of models (Tacotron2, FastSpeech2, VITS, multilingual, etc.).
Here’s a quick test:

```python
from TTS.api import TTS

# Pick a pre-trained model (Tacotron2 + DDC trained on LJSpeech dataset)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

# Convert text to audio file
tts.tts_to_file(text="Hello, I am Coqui TTS speaking from Ubuntu!", file_path="output.wav")
```

Run it:

```bash
python3 test_tts.py
```

---

## 🔹 4. Play the Sound

```bash
ffplay output.wav
```

---

## 🔹 5. Explore Available Models

You can list all available pre-trained models:

```bash
tts --list_models
```

Example output includes:

* `tts_models/en/ljspeech/tacotron2-DDC` (English, female voice)
* `tts_models/en/vctk/vits` (multi-speaker English)
* `tts_models/multilingual/multi-dataset/your_tts` (multilingual + multi-speaker)

---

✅ In short:

1. `pip install TTS`
2. `tts --list_models`
3. Use `TTS("model_name")` to load a pretrained model.
4. Generate `.wav` audio from text.

---

👉 Do you want me to give you a **list of multilingual Coqui TTS models** (like English, Hindi, Spanish, etc.) that you can download and try right away?
