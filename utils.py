from variables import secret, interval_mins, tconnect_secret, default_features

import io
import traceback
import datetime

from contextlib import redirect_stdout, redirect_stderr
from functools import wraps
from flask import request, make_response

from tconnectsync.api import TConnectApi
from tconnectsync.nightscout import NightscoutApi
from tconnectsync.sync.tandemsource.heroku_helpers import run_oneshot
from tconnectsync.features import DEFAULT_FEATURES, ALL_FEATURES

def call(fn, args, **kwargs):
    print('call args:', args)
    s = io.StringIO()
    code = 200
    with redirect_stdout(s), redirect_stderr(s):
        try:
            fn(*args, **kwargs)
        except Exception:
            traceback.print_exc(file=s)
            code = 500
    
    out = s.getvalue()
    print('call output:', out)

    return out, code

def as_text(*args):
    resp = make_response(*args)
    resp.mimetype = 'text/plain'
    return resp

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

def run_update(days, pretend, features):
    tconnect, nightscout = setup()
    time_start, time_end = get_time_args(days)

    if features is None:
        features = DEFAULT_FEATURES

    out, code = call(run_oneshot, [tconnect, nightscout, pretend, features, tconnect_secret, time_start, time_end])

    print('Completed with', code)
    print(out)

    return out, code

# In order, uses the features (in comma-delimited format) that are:
# - specified in the query (from the given argument)
# - specified as TCONNECTSYNC_HEROKU_FEATURES to tconnectsync-heroku
# The default value is the tconnectsync DEFAULT_FEATURES
def parse_features(features):
    ret = default_features.split(",")
    if features is not None and len(features) > 0:
        ret = features.split(",")
    
    ret = [i.strip() for i in ret]
    for f in ret:
        if f not in ALL_FEATURES:
            raise RuntimeError("The feature '%s' was not recognized by tconnectsync. It is not one of: %s" % (f, str(ALL_FEATURES)))
    return ret
