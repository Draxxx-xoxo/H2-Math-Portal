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
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function

admin = Blueprint('admin', __name__,
                        template_folder='templates')


@admin.route('/add_user', methods=["GET", "POST"])
def add_student():
    return render_template('add_user.html', title="Add Student")

@admin.route('/add_question', methods=["GET", "POST"])
def add_question():
    return render_template('add_question.html', title="Add Question")

@admin.route('/add_quiz', methods=["GET", "POST"])
@authorization_required
def add_quiz():
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







