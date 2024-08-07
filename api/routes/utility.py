from flask import Flask, jsonify, Blueprint # type: ignore
from datetime import datetime
import pytz

utility = Blueprint('utility', __name__)

@utility.route('/current_time')
def current_time():
    tz = pytz.timezone('Asia/Singapore')
    now = datetime.now(tz)
    return jsonify({
        'current_time': str(now)
    })