import os

secret = os.environ.get('TCONNECTSYNC_HEROKU_SECRET')
if not secret:
    print("The TCONNECTSYNC_HEROKU_SECRET environment variable is undefined,")
    print("so the API endpoints will not be accessible.")
    secret = None

interval_mins = os.environ.get('TCONNECTSYNC_HEROKU_INTERVAL_MINS')
if interval_mins:
    interval_mins = int(interval_mins)
    if interval_mins < 1:
        interval_mins = None

if not interval_mins:
    print("The TCONNECTSYNC_HEROKU_INTERVAL_MINS environment variable is undefined,")
    print("so tconnectsync will not run automatically")
    interval_mins = None

try:
    from tconnectsync import secret as tconnect_secret
except Exception as e:
    print("Tconnect environment variables are undefined.")
    print("Please follow the setup instructions at:")
    print("https://github.com/jwoglom/tconnectsync-heroku")
    raise e

from tconnectsync.features import DEFAULT_FEATURES as tconnectsync_default_features

default_features = os.environ.get('TCONNECTSYNC_HEROKU_FEATURES')
if not default_features:
    default_features = ",".join(tconnectsync_default_features)
    print("The TCONNECTSYNC_HEROKU_FEATURES environment variable is undefined,")
    print("so the following default tconnectsync features will be used: %s" % default_features)
