from flask import Blueprint, render_template, abort, session, flash, redirect, request, url_for, abort # type: ignore
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator
from handlers.common_functions import initalise_quiz, create_session, retrieve_question, check_answer

quiz = Blueprint('quiz', __name__,
                        template_folder='../../templates/quiz')


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

def check_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = str(kwargs.get('session_id'))
        res = supabase.table("session_quiz").select("*", count="exact").eq("session_id", session_id).eq("user", session['user']).execute()
        if res.count == 0:
            abort(403)
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function


# Creates Session and Set Values
@quiz.route('/quiz/<quiz_id>/create_session', methods=["POST"])
@authorization_required
def dashboard_route(quiz_id):
    value = create_session(supabase, session['user'], quiz_id)
    return redirect(url_for('quiz.start', session_id=value[0], quiz_id=quiz_id))

      
# Starting Page
@quiz.route('/quiz/<quiz_id>/<session_id>/start', methods=["GET", "POST"])
@authorization_required
@check_student
def start(quiz_id, session_id):

    res = supabase.table("session_quiz").select("is_active").eq("session_id", session_id).execute()
    is_active = res.data[0]['is_active']

    quiz_res = supabase.table("quiz").select("title, description").eq("quiz_id", quiz_id).execute()
    quiz_name = quiz_res.data[0]['title']
    quiz_description = quiz_res.data[0]['description']

    return render_template('start_quiz.html', quiz_id=quiz_id, session_id=session_id, is_active=is_active ,title="Start Quiz", quiz_name=quiz_name, quiz_description=quiz_description)

# Initalise Timer    
@quiz.route('/quiz/<quiz_id>/<session_id>/initalise', methods=["GET", "POST"])
@authorization_required
@check_student
def initalise(quiz_id, session_id):

    initalise_quiz(supabase, session_id, quiz_id)
    return redirect(url_for('quiz.quiz_question', quiz_id=quiz_id, session_id=session_id, question_no=1))


@quiz.route('/quiz/<quiz_id>/<session_id>/<question_no>', methods=["GET", "POST"])
@authorization_required
@check_student
def quiz_question(quiz_id, session_id, question_no):

    if question_no.isdigit():

        data = retrieve_question(quiz_id, question_no, supabase, session_id)
        return render_template('quiz.html', question=data[0], len_question=data[1], question_no=int(question_no), quiz_id=quiz_id, session_id=session_id, title="Question", correct_dict=data[2], target_time=data[3], quiz_name=data[4], quiz_description=data[5])
    else:
        abort(404)

@quiz.route('/quiz/<quiz_id>/<session_id>/view/<question_no>', methods=["GET", "POST"])
@authorization_required
@check_teacher
@check_student
def view_quiz_question(quiz_id, session_id, question_no):

    if question_no.isdigit():

        data = retrieve_question(quiz_id, question_no, supabase, session_id)
        return render_template('view_quiz.html', question=data[0], len_question=data[1], question_no=int(question_no), quiz_id=quiz_id, session_id=session_id, title="View Question", correct_dict=data[2], quiz_name=data[4], quiz_description=data[5])
    else:
        abort(404)

@quiz.route('/quiz/<quiz_id>/<session_id>/<question_no>/submit', methods=["POST"])
@authorization_required
@check_student
def question_submit(question_no, quiz_id, session_id):

    id = request.form['question_id']
    answer = request.form['answer']
    marks = request.form['marks']

    results = check_answer(marks, supabase, id, answer, session_id, question_no)

    if results == True:
        return redirect(url_for('quiz.quiz_question', question_no=int(question_no) + 1, quiz_id=quiz_id, session_id=session_id)) 
    
    return redirect(url_for('quiz.quiz_question', question_no=int(question_no), quiz_id=quiz_id, session_id=session_id))

@quiz.route('/quiz/<quiz_id>/view_completion', methods=["GET"])
@authorization_required
@check_teacher
def view_completion(quiz_id):
    
    quiz_res = supabase.rpc("teacher_view_completion_by_quiz", {"quiz_uuid": quiz_id}).execute()
    sessions = quiz_res.data

    return render_template('view_completed.html', quiz_id=quiz_id, title="Quiz Completion", sessions=sessions) #, quiz_name=quiz_name, quiz_description=quiz_description)


@quiz.route('/quiz/<quiz_id>/<session_id>/end_view', methods=["POST"])
@authorization_required
@check_student
def end_view(quiz_id, session_id):

    quiz_res = supabase.table("quiz").select("title, description").eq("quiz_id", quiz_id).execute()
    quiz_name = quiz_res.data[0]['title']
    quiz_description = quiz_res.data[0]['description']
    
    return render_template('end_quiz.html', quiz_id=quiz_id, session_id=session_id, title="End Quiz", quiz_name=quiz_name, quiz_description=quiz_description)


@quiz.route('/quiz/<quiz_id>/<session_id>/end', methods=["GET"])
@authorization_required
@check_student
def end(quiz_id, session_id):
    
    res = supabase.table("session_quiz").select("is_active").eq("session_id", session_id).execute()
    is_active = res.data[0]['is_active']
    
    if is_active == True:
        supabase.table("session_quiz").update({"is_active": False, "is_completed": True}).eq("session_id", session_id).execute()
    
    return redirect(url_for('dashboard.dashboard_route'))