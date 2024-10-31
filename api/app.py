from flask import Flask, redirect, render_template, session, url_for, flash, jsonify # type: ignore
import os
import requests # type: ignore
import sentry_sdk # type: ignore
from supabase import create_client, Client
from api.routes.dashboard import dashboard
from api.routes.auth import auth
from api.routes.cg import cg
from api.routes.leaderboard import leaderboard
from api.routes.quiz import quiz
from api.routes.admin import admin
from api.routes.error import error
from api.routes.utility import utility
from api.routes.profile import profile
from api.routes.attendance import attendance

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=os.environ.get('SENTRY_ENVIRONMENT'),
)


app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get("SESSION_KEY")
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(cg, url_prefix='/cg')
app.register_blueprint(leaderboard)
app.register_blueprint(quiz)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(error)
app.register_blueprint(utility, url_prefix='/utilities')
app.register_blueprint(profile)
app.register_blueprint(attendance, url_prefix='/attendance')


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/test')
def test():
    return render_template('test.html', title="Test")

if __name__ == "__main__":
    app.run()