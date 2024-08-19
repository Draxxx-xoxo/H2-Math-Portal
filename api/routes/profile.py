from flask import Blueprint, render_template, abort, session, flash, redirect, request # type: ignore
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

profile = Blueprint('profile', __name__,
                        template_folder='../../templates/profile')

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
    data = supabase.table("student").select("*").eq("login_user", session['user']).execute()
    user = data.data[0]

    role_res = supabase.table("admin").select("*").eq("user", session['user']).execute()

    if len(role_res.data) == 0:
        user['role'] = "Student"
    else:
        user['role'] = "Admin"
    
    return render_template('profile.html', title="Profile", data=user)

@profile.route("/profile/set-password", methods=["GET", "POST"])
@authorization_required
def profile_password():
    
    if request.method == 'POST':
        password = request.form['password']
        try:
            response = supabase.auth.update_user(attributes={"password": password})
            flash("Password updated successfully", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
            
    return render_template('profile_update_password.html', title="Profile")

@profile.route("/profile/set-email", methods=["GET", "POST"])
@authorization_required
def profile_email():
    
    if request.method == 'POST':
        email = request.form['email']
        try:
            response = supabase.auth.update_user(attributes={"email": email})
            flash("Email updated successfully", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")

    return render_template('profile_update_email.html', title="Profile")