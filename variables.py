import os

secret = os.environ.get('TCONNECTSYNC_HEROKU_SECRET')
if not secret:
    print("The TCONNECTSYNC_HEROKU_SECRET environment variable is undefined,")
    print("so the API endpoints will not be accessible.")
    secret = None

interval_mins = os.environ.get('TCONNECTSYNC_HEROKU_INTERVAL_MINS')
if interval_mins:
    interval_mins = int(interval_mins)
else:
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