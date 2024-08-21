from flask import Blueprint, render_template, abort, session, flash, redirect, request, url_for # type: ignore
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator

attendance = Blueprint('attendance', __name__,
                        template_folder='../../templates/attendance')

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

def check_teacher(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        teacher_res = supabase.table("teacher").select('*', count="exact").eq("user", session['user']).execute()
        if teacher_res.count == 0:
            abort(403)
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function

@attendance.route("/student", methods=["GET", "POST"])
@authorization_required
def student_attendance():
    if request.method == "POST":
        code = request.form['code']
        res = supabase.table('attendance').select("*", count="exact").eq("user", session['user']).eq("generated_code", code).execute()
        if res.count > 0:
            flash("Attendance already taken", "error")
            return redirect(url_for('attendance.student_attendance'))
        res = supabase.table('attendance_code').select("*", count="exact").eq("generated_code", code).eq("is_active", True).execute()
        if res.count == 0:
            flash("Invalid Code", "error")
            return redirect(url_for('attendance.student_attendance'))
        else:
            res = supabase.table('attendance').insert({"user": session['user'], "generated_code": code}).execute()
            flash("Attendance Taken", "success")
            return redirect(url_for('attendance.student_attendance'))
        
    return render_template('student_attendance.html', title="Student Attendance")

@attendance.route("/teacher")
@authorization_required
@check_teacher
def teacher_attendance():
    return render_template('teacher_attendance.html', title="Teacher Attendance")
