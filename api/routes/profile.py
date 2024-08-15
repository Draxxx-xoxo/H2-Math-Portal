from flask import Blueprint, render_template, abort, session, flash, redirect, request # type: ignore
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

profile = Blueprint('profile', __name__,
                        template_folder='../../templates')

def is_authorized():
    if 'user' not in session:
        return False
    return True

def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            access_token = session['access_token']
            refresh_token = session['refresh_token']
            res = supabase.auth.set_session(access_token, refresh_token)

        except:
            return redirect('/login')  # Redirect to login if not authorized
        
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)


@profile.route("/profile")
@authorization_required
def profile_main():
    return render_template('profile.html', title="Profile")

@profile.route("/profile/set-password", methods=["GET", "POST"])
@authorization_required
def profile_password():
    return render_template('profile_update_password.html', title="Profile")

@profile.route("/profile/set-email", methods=["GET", "POST"])
@authorization_required
def profile_email():
    return render_template('profile_update_email.html', title="Profile")