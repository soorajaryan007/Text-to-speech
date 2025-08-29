from flask import Flask, render_template, request, jsonify
from TTS.api import TTS
from time import time
import os
from uuid import uuid4

from db import init_db, get_db_session
from models import History

app = Flask(__name__)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static')

# Load the pre-trained Coqui TTS model once
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=False)  # set gpu=True if you have GPU

# Initialize database
init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form['text'].strip()
        lang = request.form.get('lang', 'en')
        if text:
            # Generate a unique file for current request
            ts = int(time())
            output_filename = f"output_{ts}.wav"
            output_path = os.path.join(AUDIO_DIR, output_filename)
            tts.tts_to_file(text=text, file_path=output_path)
            audio_file = f"static/{output_filename}"

            # Save to DB
            db = get_db_session()
            try:
                entry = History(
                    id=str(uuid4()),
                    text=text[:2000],
                    lang=lang,
                    file=audio_file,
                    created_at=ts,
                )
                db.add(entry)
                # Keep only latest 100 by deleting older ones (optional)
                db.commit()
            finally:
                db.close()

    # Load recent history
    db = get_db_session()
    try:
        recent = db.query(History).order_by(History.created_at.desc()).limit(20).all()
        recent_history = [
            {
                'id': h.id,
                'text': h.text,
                'lang': h.lang,
                'file': h.file,
                'created_at': h.created_at,
            }
            for h in recent
        ]
    finally:
        db.close()

    return render_template('index.html', audio_file=audio_file, error=None, selected_lang='en', recent_history=recent_history)


@app.route('/history', methods=['GET'])
def list_history():
    db = get_db_session()
    try:
        items = db.query(History).order_by(History.created_at.desc()).all()
        return jsonify([
            {
                'id': h.id,
                'text': h.text,
                'lang': h.lang,
                'file': h.file,
                'created_at': h.created_at,
            }
            for h in items
        ])
    finally:
        db.close()


@app.route('/history/<entry_id>', methods=['DELETE'])
def delete_history(entry_id):
    db = get_db_session()
    try:
        h = db.query(History).filter(History.id == entry_id).first()
        if not h:
            return jsonify({"ok": False, "error": "Not found"}), 404
        # Delete file if exists
        try:
            file_path = h.file
            if file_path and file_path.startswith('static/'):
                os.remove(os.path.join(os.path.dirname(__file__), file_path))
        except Exception:
            pass
        db.delete(h)
        db.commit()
        return jsonify({"ok": True})
    finally:
        db.close()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

