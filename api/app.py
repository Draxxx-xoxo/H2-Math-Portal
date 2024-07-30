from flask import Flask, redirect, render_template, session, url_for, flash, jsonify
import os
import requests
import sentry_sdk
from datetime import datetime
from supabase import create_client, Client
from functools import wraps  # Import wraps decorator
from api.routes.dashboard import dashboard
from api.routes.auth import auth
from api.routes.cg import cg
from api.routes.leaderboard import leaderboard
from api.routes.quiz import quiz

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=os.environ.get('SENTRY_ENVIRONMENT'),
)


app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_KEY")
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(cg, url_prefix='/cg')
app.register_blueprint(leaderboard)
app.register_blueprint(quiz)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

app.config['supabase'] = supabase

def is_authorized():
    if 'user' not in session:
        return False
    return True

def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authorized():
            flash("You are not authorized to access this page.", "error")
            return redirect('/login')  # Redirect to login if not authorized
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html', title="Home")


@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html", title="404") 


if __name__ == "__main__":
    app.run(debug=True)