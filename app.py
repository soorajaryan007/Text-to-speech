from flask import Flask, render_template, request
from TTS.api import TTS
from time import time
import os, glob

app = Flask(__name__)

# Load the pre-trained Coqui TTS model once
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=False)  # set gpu=True if you have GPU


@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form['text'].strip()
        if text:
            # Remove old audio files to avoid clutter
            for f in glob.glob("static/output_*.wav"):
                os.remove(f)
            # Generate a unique file for current request
            output_path = f"static/output_{int(time())}.wav"
            tts.tts_to_file(text=text, file_path=output_path)
            audio_file = output_path
    return render_template(
        'index.html',
        audio_file=audio_file,
        error=None,
        selected_lang='en'
    )


if __name__ == '__main__':
    app.run(debug=True)

