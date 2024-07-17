from flask import Flask, redirect, render_template, session, url_for, flash
import csv
import json
import os
from datetime import datetime
from supabase import create_client, Client
from functools import wraps  # Import wraps decorator
from api.routes.dashboard import dashboard
from api.routes.auth import auth

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.register_blueprint(dashboard)
app.register_blueprint(auth)

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
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)