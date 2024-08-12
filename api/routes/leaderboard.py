from flask import Blueprint, render_template, abort, session, flash, redirect, request # type: ignore
import csv
import json
import os
from supabase import create_client, Client
from datetime import datetime

leaderboard = Blueprint('leaderboard', __name__,
                        template_folder="../../templates")


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)


@leaderboard.route('/leaderboard')
def dashboard_route():
    
    response = supabase.table("leaderboard").select("*").order("points", desc=True).execute()
    students = response.data
    return render_template("leaderboard.html", students=students, title="Leaderboard")


