from flask import Blueprint, render_template, abort, session, flash, redirect, request, url_for, abort # type: ignore
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator
from api.handlers.common_functions import initalise_quiz, create_session, retrieve_question, check_answer
import numpy as np
from numpy import random

quiz = Blueprint('quiz', __name__,
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
def start(quiz_id, session_id):

    return render_template('start_quiz.html', quiz_id=quiz_id, session_id=session_id, title="Start Quiz")

# Initalise Timer    
@quiz.route('/quiz/<quiz_id>/<session_id>/initalise', methods=["GET", "POST"])
def initalise(quiz_id, session_id):

    #questions = initalise_quiz(supabase, "10e912fc-3f86-4e42-8394-b21b19019bf1", a, b, c)
    return redirect(url_for('quiz.quiz_question', quiz_id=quiz_id, session_id=session_id, question_no=1))


@quiz.route('/quiz/<quiz_id>/<session_id>/<question_no>', methods=["GET", "POST"])
def quiz_question(quiz_id, session_id, question_no):

    if question_no.isdigit():

        question = retrieve_question(quiz_id, question_no, supabase, session_id)

        return render_template('quiz.html', question=question, len_question=int("4"), question_no=int(question_no), quiz_id=quiz_id, session_id=session_id, title="Question")
    else:
        abort(404)



@quiz.route('/quiz/<quiz_id>/<session_id>/<question_no>/submit', methods=["POST"])
def question_submit(question_no, quiz_id, session_id):

    id = request.form['question_id']
    print(id)
    answer = request.form['answer']

    results = check_answer(supabase, id, answer, session_id, question_no)

    if results == True:
        return redirect(url_for('quiz.quiz_question', question_no=int(question_no) + 1, quiz_id=quiz_id, session_id=session_id)) 
    
    return redirect(url_for('quiz.quiz_question', question_no=int(question_no), quiz_id=quiz_id, session_id=session_id))

