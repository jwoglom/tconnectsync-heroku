# TConnectSync for Heroku

This project allows [tconnectsync][tconnectsync] to run in Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jwoglom/tconnectsync-heroku)

You can use the Heroku free plan.
You should have enough monthly dyno minutes available to run the app continuously
if you provide a credit card to your account.

## Setup

Start by clicking the button above to deploy the app to Heroku.
You will need to set Heroku environment variables for tconnectsync options
([see the tconnect environment variables documentation][tconnect-installation]):

* TCONNECT_EMAIL
* TCONNECT_PASSWORD
* NS_URL
* NS_SECRET
* PUMP_SERIAL_NUMBER
* TIMEZONE_NAME

You can invoke the application in one of two ways:

## UptimeRobot
You should specify the following environment variable:

* TCONNECTSYNC_HEROKU_SECRET - a secret password which can be used to access
  API endpoints for the web application. (optional)

Restart the app in heroku after setting environment variables.

Then, create an account at [UptimeRobot][uptimerobot] and use the following
check URL:

```
https://YOUR-APPLICATION-SUBDOMAIN-HERE.heroku.io/run?secret=YOUR-SECRET-PASSWORD
```

Specify a check interval of 30 minutes, or however frequently you would like tconnectsync to run.


## Background Tasks
You should specify the following environment variable:

* TCONNECTSYNC_HEROKU_INTERVAL_MINS - The interval at which a scheduled task should
  be performed for a synchronization. This will **only** function while the Flask
  application is running. (Heroku will shut down the app after some period of
  inactivity.)

You may also wish to configure the TCONNECTSYNC_HEROKU_SECRET environment variable
as well (described above).

When the Flask application is started, so long as it is running the tconnect
synchronization task will run at the given interval.

Note that **Heroku may shut down your dyno if it has not processed requests in
30 minutes**.

You should ideally set up UptimeRobot to ping your application at the index URL
(**not** the run endpoint, since that will cause the synchronization to happen
both triggered by UptimeRobot and the background task daemon itself):

```
https://YOUR-APPLICATION-SUBDOMAIN-HERE.heroku.io/
```


## Testing

You can hit the following URL to verify that your tconnectsync options are
specified correctly, and that both TConnect and Nightscout are accessible:

```
https://YOUR-APPLICATION-SUBDOMAIN-HERE.heroku.io/check_login?secret=YOUR-SECRET-PASSWORD
```


[tconnectsync]: https://github.com/jwoglom/tconnectsync
[tconnect-installation]: https://github.com/jwoglom/tconnectsync#installation
[uptimerobot]: https://uptimerobot.com/

## Updating to a new version

To update your Heroku instance of tconnectsync, perform the following steps.
This is a tconnectsync specific version of the "Deploy using Heroku Git"
instructions which are present in the "Deploy" tab of your Heroku console.

1.  [Install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2.  In a terminal, clone your Heroku repository and pull the latest version of tconnectsync-heroku:
    ```
    heroku git:clone -a YOUR_HEROKU_SITE_NAME
    cd YOUR_HEROKU_SITE_NAME
    git remote add upstream https://github.com/jwoglom/tconnectsync-heroku
    git pull -r upstream main
    ```
3.  Deploy the updated app to Heroku:
    ```
    git push heroku main
    ```
