from flask import Blueprint, render_template, abort, session, flash, redirect, request, url_for
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime
from functools import wraps  # Import wraps decorator
from api.handlers.common_functions import initalise_quiz, vector_calculate_area
import numpy as np

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


@quiz.route('/quiz/<quiz_id>/<session_id>')
@authorization_required
def dashboard_route():

    return render_template("leaderboard.html")


@quiz.route('/grab/<question_no>', methods=["GET", "POST"])
def grab(question_no):

    a = (1, 2, 3)
    b = (4, 5, 6)
    c = (7, 8, 9)

    questions = initalise_quiz(supabase, "10e912fc-3f86-4e42-8394-b21b19019bf1", a, b, c)
    return render_template('quiz.html', questions=questions, question_no=int(question_no) - 1, a=a, b=b, c=c)



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

