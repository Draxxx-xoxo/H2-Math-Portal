from flask import Blueprint, render_template, abort, session, flash, redirect, request # type: ignore
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

dashboard = Blueprint('dashboard', __name__,
                        template_folder='../../templates/dashboard')

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


@dashboard.route('/dashboard')
@authorization_required 
def dashboard_route():
    response = supabase.table("student").select("cg").eq("login_user", session['user']).execute()
    cg = (response.data[0]['cg'])
    cg_link = cg.replace("/", "_")

    role_res = supabase.table("admin").select("*").eq("user", session['user']).execute()
    role = ""

    quiz_res = supabase.table("quiz").select("title, description, quiz_id").order("id", desc=False).execute()
    quiz_list = quiz_res.data

    quiz_session_res = supabase.table('session_quiz').select('quiz_id, session_id, is_completed').eq('user', session['user']).execute()
    lis_quiz_id = [[],{}, {}]

    for quiz in quiz_session_res.data:
        lis_quiz_id[0].append(quiz['quiz_id'])
        lis_quiz_id[1][quiz['quiz_id']] = quiz['session_id']
        lis_quiz_id[2][quiz['quiz_id']] = quiz['is_completed']

    if len(role_res.data) == 0:
        role = "user"
    else:
        role = "admin"    

    return render_template("dashboard.html", cg=cg, cg_link=cg_link, title="Dashboard", role=role, quiz_list=quiz_list, created_quiz=lis_quiz_id)


