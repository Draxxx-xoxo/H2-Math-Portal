from flask import Blueprint, render_template, abort, session, flash, redirect, request # type: ignore
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

cg = Blueprint('cg', __name__,
                        template_folder='templates')

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


        cg = str(kwargs.get('cg')).replace("_", "/")

        try:
            id = session['user']
        except:
            id = None
        
        response = supabase.table("student").select("cg").eq("login_user", id).eq("cg", cg).execute()

        if len(response.data) == 0:
            return abort(403)  # Redirect to forbidden if not authorized
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function


@cg.route('/<cg>')
@authorization_required
def dashboard_route(cg):

    cg = cg.replace("_", "/")
    response = supabase.table("student").select("*").eq("cg", cg).execute()
    students = response.data   

    return render_template("cg.html", students=students, title="Civic Group")


