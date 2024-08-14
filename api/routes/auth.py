from urllib.parse import quote_plus, urlencode
from flask import Blueprint, render_template, abort, session, flash, redirect, url_for, request # type: ignore
from jinja2 import TemplateNotFound # type: ignore
import os
from supabase import create_client, Client
from functools import wraps  # Import wraps decorator

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

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

auth = Blueprint('auth', __name__,
                        template_folder='../../templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['login'] == 'login':
            email = request.form['email']
            password = request.form['password']
            try:
                data = supabase.auth.sign_in_with_password({"email": email, "password": password})

                session['user'] = data.user.id
                session['access_token'] = data.session.access_token
                session['refresh_token'] = data.session.refresh_token

                flash("Login successful!", "success")
                return redirect('/dashboard')
            
            except Exception as e:
                flash(f"Login error: {e}", "error")

        elif request.form['login'] == "reset":
            email = request.form['email']
            try:
                supabase.auth.reset_password_email(email=email, options={'redirect_to': 'http://localhost:3000/update-password'})
                flash("Password reset email sent.", "success")
            except Exception as e:
                flash(f"Error: {e}", "error")

    if 'user' in session:
        return redirect('/dashboard')
    
    return render_template('login.html', title="Login")

@auth.route('/update-password', methods=['GET', 'POST'])
def update_password():
    return render_template('update_password.html', title="Update Password")

@auth.route('/signout')
@authorization_required 
def signout():
    try:
        supabase.auth.sign_out()
        session.clear()
        flash("Signout successful.", "success")
    except Exception as e:
        flash(f"Signout error: {e}", "error")

    return redirect('/')








