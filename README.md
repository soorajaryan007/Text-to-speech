# Voice.AI – Text-to-Speech Web App

![Work in Progress](https://img.shields.io/badge/status-WIP-yellow)

> This project is currently under development. Features may change frequently.


# Voice.AI – Text-to-Speech Web App

A simple **Text-to-Speech (TTS) web application** built with **Flask** and **Coqui TTS**. Users can type text into a web form and get a **voice output** in real time.

---

## Features

* Convert typed text into speech using **pre-trained Coqui TTS models**.
* Automatically generates a **.wav audio file** for each input.
* Removes old audio files to prevent clutter.
* Lightweight and easy to run locally.

---

## Demo

![demo image](optional-you-can-add-screenshot.png)

---

## Installation

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd tts_web_app
```

2. **Create and activate a virtual environment (optional but recommended)**:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install Flask TTS
```

---

## Usage

1. Make sure you have a folder named `static/` in the project root (audio files will be saved there).

2. Run the Flask app:

```bash
python app.py
```

3. Open your browser and go to:

```
http://127.0.0.1:5000/
```

4. Type text into the input box and click **Convert to Speech**. The generated audio will appear below the form and play automatically.

---

## Project Structure

```
tts_web_app/
├── app.py              # Main Flask app
├── templates/
│   └── index.html      # Frontend HTML template
├── static/             # Generated audio files
└── README.md
```

---

## Notes

* The app uses the **`tts_models/en/ljspeech/tacotron2-DDC`** pre-trained Coqui TTS model.
* You can change the model to another supported one if needed.
* Set `gpu=True` in `TTS()` if you have a GPU to speed up generation.

---

## License

This project is open-source 
