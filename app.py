"""Wrapper for tconnectsync running in Heroku."""

from variables import secret, interval_mins, tconnect_secret
from utils import token_required, call, setup, get_time_args, run_update, as_text, parse_features

from threading import Thread
from flask import Flask, request
from flask.templating import render_template
from flask_apscheduler import APScheduler
from flask_apscheduler.auth import HTTPBasicAuth

from tconnectsync.check import check_login
from tconnectsync import __version__ as tconnectsync_version

version = '0.3.1'
print("Launching tconnectsync-heroku %s" % str(version))
print("Using tconnectsync %s" % str(tconnectsync_version))

app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.auth = HTTPBasicAuth()
scheduler.init_app(app)
scheduler.start()

@scheduler.authenticate
def authenticate(auth):
    if not secret:
        return False

    return auth["password"] == secret

@app.route('/')
def index_route():
    job = scheduler.get_job('update')
    return render_template('index.html', 
        tconnectsyncheroku_version=version,
        tconnectsync_version=tconnectsync_version,
        job=job,
        interval_mins=interval_mins)

"""Runs the tconnectsync login check synchronously, returning the result."""
@app.route('/check_login')
@token_required
def check_login_route():
    tconnect, _ = setup()
    time_start, time_end = get_time_args(request.values.get("days"))
    return as_text(*call(check_login, [tconnect, time_start, time_end, True]))

"""Runs tconnectsync synchronously, returning the result."""
@app.route('/update')
@token_required
def update_route():
    days = request.values.get("days")
    pretend = bool(request.values.get("pretend"))
    features = parse_features(request.values.get("features"))
    return as_text(*run_update(days, pretend, features))

"""Runs tconnectsync in the background, does not return an error if one occurs."""
@app.route('/run')
@token_required
def run_route():
    days = request.values.get("days")
    pretend = bool(request.values.get("pretend"))
    features = parse_features(request.values.get("features"))
    Thread(target=run_update, kwargs={'days': days, 'pretend': pretend, 'features': features}).start()
    return 'Triggered job'

if interval_mins:
    print("Creating scheduled task for every", interval_mins, "minutes")
    @scheduler.task('interval', id='update', seconds=interval_mins * 60, misfire_grace_time=300)
    def scheduled_update_task():
        print('Running update scheduler task')
        run_update(1, False, parse_features(None))
        print('Finished update scheduler task')

if __name__ == '__main__':
    import os
    LISTEN_HOST = os.getenv('LISTEN_HOST', '0.0.0.0')
    LISTEN_PORT = int(os.getenv('LISTEN_PORT', '5000'))
    app.run(LISTEN_HOST, LISTEN_PORT)
