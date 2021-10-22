from variables import secret, interval_mins, tconnect_secret

import io
import traceback
import datetime

from contextlib import redirect_stdout, redirect_stderr
from functools import wraps
from flask import request

from tconnectsync.api import TConnectApi
from tconnectsync.nightscout import NightscoutApi
from tconnectsync.process import process_time_range

def call(fn, args):
    print('call args:', args)
    s = io.StringIO()
    code = 200
    with redirect_stdout(s), redirect_stderr(s):
        try:
            fn(*args)
        except Exception:
            traceback.print_exc(file=s)
            code = 500
    
    out = s.getvalue()
    print('call output:', out)

    return out, code

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not secret:
            return "secret is not configured in the settings, so this page is inaccessible", 403
        if request.values.get("secret") is None:
            return "secret not provided as a GET or POST argument", 403
        if request.values.get("secret") != secret:
            return "secret is invalid", 403
        return f(*args, **kwargs)
    return decorated_function

def setup():
    tconnect = TConnectApi(tconnect_secret.TCONNECT_EMAIL, tconnect_secret.TCONNECT_PASSWORD)
    nightscout = NightscoutApi(tconnect_secret.NS_URL, tconnect_secret.NS_SECRET)

    return tconnect, nightscout

def get_time_args(days):
    if days:
        days = int(days)
    else:
        days = 1
    
    time_end = datetime.datetime.now()
    time_start = time_end - datetime.timedelta(days=days)

    return time_start, time_end

def run_update(days, pretend):
    tconnect, nightscout = setup()
    time_start, time_end = get_time_args(days)

    out, code = call(process_time_range, [tconnect, nightscout, time_start, time_end, pretend])

    print('Completed with', code)
    print(out)