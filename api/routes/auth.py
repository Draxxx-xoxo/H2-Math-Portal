from urllib.parse import quote_plus, urlencode
from flask import Blueprint, render_template, abort, session, flash, redirect, url_for, request, current_app as app
from jinja2 import TemplateNotFound
import os
from functools import wraps  # Import wraps decorator

def is_authorized():
    if 'user' not in session:
        return False
    return True

def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authorized():
            return redirect('/login')  # Redirect to login if not authorized
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function

auth = Blueprint('auth', __name__,
                        template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            data = app.config['supabase'].auth.sign_in_with_password({"email": email, "password": password})

            session['user'] = data.user.email
            flash("Login successful!", "success")
            return redirect('/dashboard')
        
        except Exception as e:
            flash(f"Login error: {e}", "error")

    if 'user' in session:
        return redirect('/dashboard')
    
    return render_template('login.html')


@auth.route('/signout')
@authorization_required 
def signout():
    try:
        app.config['supabase'].auth.sign_out()
        session.clear()
        flash("Signout successful.", "success")
    except Exception as e:
        flash(f"Signout error: {e}", "error")

    return redirect('/')








