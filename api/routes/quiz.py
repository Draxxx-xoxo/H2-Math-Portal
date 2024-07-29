from flask import Blueprint, render_template, abort, session, flash, redirect, request, url_for, abort
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator
from api.handlers.common_functions import initalise_quiz, vector_calculate_area, create_session, retrieve_question
import numpy as np
from numpy import random

quiz = Blueprint('quiz', __name__,
                        template_folder='templates')


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

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

    return render_template('start_quiz.html', quiz_id=quiz_id, session_id=session_id)

# Initalise Timer    
@quiz.route('/quiz/<quiz_id>/<session_id>/initalise', methods=["GET", "POST"])
def initalise(quiz_id, session_id):

    #questions = initalise_quiz(supabase, "10e912fc-3f86-4e42-8394-b21b19019bf1", a, b, c)
    return redirect(url_for('quiz.quiz_question', quiz_id=quiz_id, session_id=session_id, question_no=1))


@quiz.route('/quiz/<quiz_id>/<session_id>/<question_no>', methods=["GET", "POST"])
def quiz_question(quiz_id, session_id, question_no):

    if question_no.isdigit():

        question = retrieve_question(quiz_id, question_no, supabase, session_id)

        return render_template('quiz.html', question=question, len_question=int("4"), a="", b="", c="", question_no=int(question_no), quiz_id=quiz_id, session_id=session_id)
    else:
        abort(404)



@quiz.route('/grab/<question_no>/submit', methods=["POST"])
def grab_submit(question_no):

    id = request.form['question_id']
    answer = request.form['answer']
    a = request.form['a']
    b = request.form['b']
    c = request.form['c']

    results = vector_calculate_area(a, b, c, answer)

    if results == True:
        return redirect(url_for('quiz.grab', question_no=int(question_no) + 1))
    
    return redirect(url_for('quiz.grab', question_no=int(question_no)))

