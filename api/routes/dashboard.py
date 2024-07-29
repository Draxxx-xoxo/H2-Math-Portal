from flask import Blueprint, render_template, abort, session, flash, redirect, request
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

dashboard = Blueprint('dashboard', __name__,
                        template_folder='templates')


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

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)


@dashboard.route('/dashboard')
@authorization_required 
def dashboard_route():
    email = session['user']
    response = supabase.table("students").select("cg, email").eq("login_user", session['user']).execute()
    cg = (response.data[0]['cg'])
    cg_link = cg.replace("/", "_")
    return render_template("dashboard.html", cg=cg, cg_link=cg_link)


