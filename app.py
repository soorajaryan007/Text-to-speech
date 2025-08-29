from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from TTS.api import TTS
from time import time
import os, glob, json

from authlib.integrations.flask_client import OAuth  # type: ignore

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

# Load users from disk (keyed by email or login)
if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except Exception:
        users = {}
else:
    users = {}


def save_users() -> None:
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
    except Exception:
        pass


# OAuth configuration for GitHub
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
OAUTH_REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI')  # e.g., http://127.0.0.1:5000/auth/callback

oauth = OAuth(app)
if GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:
    oauth.register(
        name='github',
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'read:user user:email'}
    )


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
        selected_lang='en',
        logged_in=('user_login' in session or 'user_email' in session),
        user_email=session.get('user_email'),
        user_login=session.get('user_login'),
        oauth_ready=bool(GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET and OAUTH_REDIRECT_URI)
    )


@app.route('/login/github')
def login_github():
    if not (GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET):
        return jsonify({"ok": False, "error": "GitHub OAuth is not configured. Set GITHUB_CLIENT_ID/SECRET and GITHUB_REDIRECT_URI."}), 500
    redirect_uri = OAUTH_REDIRECT_URI or url_for('auth_callback', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@app.route('/auth/callback')
def auth_callback():
    if not (GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET):
        return redirect(url_for('index'))
    token = oauth.github.authorize_access_token()
    user = oauth.github.get('user').json()
    emails = oauth.github.get('user/emails').json() if token else []

    login = user.get('login')
    name = user.get('name') or login
    email = None
    if isinstance(emails, list):
        primary = next((e for e in emails if e.get('primary')), None)
        email = (primary or (emails[0] if emails else {})).get('email')

    key = email or login
    if key:
        if key not in users:
            users[key] = {"login": login, "name": name, "email": email}
            save_users()
        session['user_login'] = login
        session['user_name'] = name
        if email:
            session['user_email'] = email
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_email', None)
    session.pop('user_login', None)
    session.pop('user_name', None)
    return jsonify({"ok": True})


if __name__ == '__main__':
    app.run(debug=True)

