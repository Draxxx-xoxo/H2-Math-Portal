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


@dashboard.route('/dashboard')
@authorization_required 
def dashboard_route():
    return render_template("dashboard.html")


