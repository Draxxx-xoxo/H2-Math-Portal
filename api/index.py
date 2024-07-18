from flask import Flask, redirect, render_template, session, url_for, flash, jsonify
import csv
import json
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from supabase import create_client, Client
from functools import wraps  # Import wraps decorator
from api.routes.dashboard import dashboard
from api.routes.auth import auth
import stripe
stripe.api_key = os.environ.get("STIPE_API_KEY")

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.register_blueprint(dashboard)
app.register_blueprint(auth)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

app.config['supabase'] = supabase

def is_authorized():
    if 'user' not in session:
        return False
    return True

def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authorized():
            flash("You are not authorized to access this page.", "error")
            return redirect('/login')  # Redirect to login if not authorized
        return f(*args, **kwargs)  # Allow access to the route
    return decorated_function

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/pricing')
def pricing():
    print(session['user'])
    return render_template('stripe_pt.html', email=session['user'] )


@app.route('/create-customer-portal-session', methods=['POST'])
def customer_portal():

    try:
        response = requests.get(
            'https://api.stripe.com/v1/customers',
            params={'email': session['user']},
            headers={'Authorization': f'Bearer {os.environ.get("STIPE_API_KEY")}'}
        )

        if response.status_code == 200:
            results = response.json()

            if 'data' in results and len(results['data']) > 0:
                customer_id = results['data'][0]['id']

                portal_session = stripe.billing_portal.Session.create(
                    customer=customer_id,
                    return_url="https://supabase-flask.vercel.app/dashboard",
                )

                return redirect(portal_session.url)

            else:
                return jsonify({'error': 'No customer found with the provided email'}), 404

        else:
            return jsonify({'error': 'Failed to retrieve customer data from Stripe'}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)