from flask import Flask, jsonify, Blueprint, session, redirect, request # type: ignore
import os
from datetime import datetime
import pytz
from functools import wraps  # Import wraps decorator
from supabase import create_client, Client

utility = Blueprint('utility', __name__)

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

@utility.route('/current_time')
def current_time():
    tz = pytz.timezone('Asia/Singapore')
    now = datetime.now(tz)
    return jsonify({
        'current_time': str(now)
    })

@utility.route('/insert_code', methods=["POST"])
@authorization_required
def insert_code():
    data = request.get_json()
    code = data['code']
    try:
        res = supabase.table('attendance_code').insert({"generated_code": code, "user": session['user']}).execute()
        return "Code inserted", 200
    except Exception as e:
        return str(e), 500
    
@utility.route('/delete_code', methods=["POST"])
@authorization_required
def delete_code():
    data = request.get_json()
    code = data['code']
    try:
        res = supabase.table('attendance_code').update({"is_active": False}).eq("generated_code", code).execute()
        return "Code Deleted", 200
    except Exception as e:
        return str(e), 500
    
