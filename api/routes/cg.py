from flask import Blueprint, render_template, abort, session, flash, redirect, request
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

cg = Blueprint('cg', __name__,
                        template_folder='templates')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)


def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cg = str(kwargs.get('cg')).replace("_", "/")

        try:
            id = session['user']
        except:
            id = None
            
        if 'user' not in session:
            return redirect('/login')
        
        response = supabase.table("students").select("cg, email").eq("login_user", id).eq("cg", cg).execute()

        if len(response.data) == 0:
            return render_template("forbidden.html", title="Forbidden")
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function


@cg.route('/<cg>')
@authorization_required
def dashboard_route(cg):

    cg = cg.replace("_", "/")
    response = supabase.table("students").select("*").eq("cg", cg).execute()
    students = response.data   

    return render_template("cg.html", students=students, title="Civic Group")


