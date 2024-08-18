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
        
        role_res = supabase.table("admin").select("*").eq("user", session['user']).execute()

        if len(role_res.data) == 0:
            return abort(403)  # Redirect to forbidden if not authorized
               
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function

admin = Blueprint('admin', __name__,
                        template_folder='../../templates')


@admin.route('/add_user', methods=["GET", "POST"])
@authorization_required
def add_student():

    cgs = supabase.table("cg").select("*").execute()
    cgs = cgs.data
    
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cg = request.form['cg']
        phone_num = request.form['phone-num']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        try:
            response = supabase.auth.sign_up(credentials={"email": email, "password": password})
            login_user_id = response.user.id
            if role == "admin":
                supabase.table("admin").insert({"user": login_user_id}).execute()
            elif role == "student":
                supabase.table("leaderboard").insert({"user": login_user_id}).execute()
                supabase.table("student").insert({"cg": cg, "phone_number": phone_num, "name": first_name + " " + last_name, "login_user": login_user_id, "leaderboard_user": login_user_id }).execute()
                flash("Student added successfully", "success")
            
            flash("Student added successfully", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")

    return render_template('add_user.html', title="Add Student" , cgs=cgs)

@admin.route('/add_question', methods=["GET", "POST"])
@authorization_required
def add_question():

    if request.method == 'POST':
        question = request.form['question']
        marks = request.form['marks']
        topic = request.form['topic']
        try:
            supabase.table("question").insert({"question": question, "marks": int(marks), "topic": topic}).execute()
            #flash("Question added successfully", "success")
        except Exception as e:
            #flash(f"Error: {e}", "error")
            print(e)

    return render_template('add_question.html', title="Add Question")

@admin.route('/add_quiz', methods=["GET", "POST"])
@authorization_required
def add_quiz():

    if request.method == 'POST':
        questions_id = request.form.getlist('questions')
        title = request.form['title']
        description = request.form['description']
        time_limit = request.form['time-limit']
        try:
            response = supabase.table("quiz").insert({"title": title, "description": description, "time_limit": time_limit, "question_count": len(questions_id)}).execute()
            count = 1
            for id in questions_id:
                supabase.table("quiz").update({f"question_{count}": id}).eq("quiz_id", response.data[0]['quiz_id']).execute()
                count += 1
            #flash("Quiz added successfully", "success")
        except Exception as e:
            print(e)
            #flash(f"Error: {e}", "error")

    question_lis = []
    questions = supabase.table("question").select("*").execute()
    for question in questions.data:
        question_dict = {
            "question": question['question'],
            "marks": question['marks'],
            "topic": question['topic'],
            "id": question['question_id']
        }
        question_lis.append(question_dict)
    return render_template('add_quiz.html', title="Add Quiz", questions=question_lis)







