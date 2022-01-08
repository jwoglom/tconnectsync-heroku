# TConnectSync for Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jwoglom/tconnectsync-heroku)

This project allows [tconnectsync][tconnectsync] to run in Heroku.
It supports the Heroku Free Plan: you should have enough monthly dyno minutes
available to run the app continuously if you provide a credit card to your account.

## Setup

Before beginning, make sure you have set up the t:connect
[Android](https://play.google.com/store/apps/details?id=com.tandemdiabetes.tconnect&hl=en_US&gl=US), 
or [iPhone/iOS](https://apps.apple.com/us/app/t-connect-mobile/id1455916023) application.
If you have not used either, you can find more information or create an account [at the t:connect website]([t:connect web](https://tconnect.tandemdiabetes.com/).

You'll need the following information:

* Your t:connect username and password
* Your t:slim X2 pump serial number (visible in Settings > My Pump > Pump Info)
* Your Nightscout site URL
* Your Nightscout site secret

If you have not yet set up a Nightscout site, [view the Nightscout documentation and set that up first](https://nightscout.github.io/nightscout/new_user/), then come back to these instructions.
Either log in to your existing Heroku account or create a new one.

Next, you'll be creating a new application inside your Heroku account.
This will not be replacing your existing Heroku Nightscout app, if you have one; you will
be creating a second app with a new name.
Start by clicking the Deploy button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jwoglom/tconnectsync-heroku)

For *App name*, you can enter any value, such as `YourExistingNightscoutAppName-tconnect`.
The app name determines the URL to access your tconnectsync-heroku website, which will be
e.g. `YourExistingNightscoutAppName-tconnect.herokuapp.com`.
This **tconnectsync Heroku App URL** will be referred to as `https://YOUR-TCONNECTSYNC-APP-NAME.herokuapp.com` for the remainder of the guide.

The remainder of the options are ([tconnectsync environment variables][tconnect-installation]):

* `TCONNECT_EMAIL` - Your t:connect email
* `TCONNECT_PASSWORD` - Your t:connect password
* `NS_URL` - Your Nightscout site URL (e.g. https://yournightscoutsite.herokuapp.com)
* `NS_SECRET` - Your Nightscout `API_SECRET` value
* `PUMP_SERIAL_NUMBER` - The numeric serial number of your pump
* `TIMEZONE_NAME` - The timezone code in which your phone and pump's time is set. ([View a full list of valid values](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))

A new variable called `TCONNECTSYNC_HEROKU_SECRET` will be automatically generated for you.
This secret password will be used to access API endpoints which trigger your pump data from tconnect
to be synchronized to Nightscout, as well as view the current status of synchronization.
(You can think of it like the tconnectsync equivalent to Nightscout's `API_SECRET`.)
You can find its automatically generated value by going to Settings > Reveal Config Vars in your Heroku dashboard after setup.

Once you've filled out the Create New App form and pressed *Deploy App*, you'll be taken to the Heroku dashboard.
The remainder of the steps required involve creating an account with a separate service, **UptimeRobot**.

## UptimeRobot

Even though your Heroku app is already up and running, we need to set up a service called **UptimeRobot**
which will send a request to your Heroku app to keep it alive so that it can continue to process
your incoming t:connect data in the background.

First, go into your Heroku dashboard and select the app you created for tconnectsync.
Click on Settings > Reveal Config Vars and copy the value of `TCONNECTSYNC_HEROKU_SECRET`,
which will be in a text box to the right of `TCONNECTSYNC_HEROKU_SECRET`.

If you'd like, you can change the value here to a different password.
If so, then save settings and then restart the app in heroku. (More > Restart All Dynos).

Then, create an account at [UptimeRobot][uptimerobot].
Once you register, log in and click **Add New Monitor**.

Enter the following:

* Monitor Type: **HTTP(s)**
* Friendly Name: **tconnectsync**
* Monitoring Interval: **every 30 minutes**
* Monitor Timeout: **1 minute**

Enter the following as the URL:
```
https://YOUR-TCONNECTSYNC-APP-NAME.herokuapp.com/run?secret=YOUR_TCONNECTSYNC_HEROKU_SECRET_VALUE
```

Click **Create Monitor**.
Now, every 30 minutes, tconnectsync will be triggered to synchronize your data between t:connect and Nightscout!


## Testing

You can hit the following URL to verify that your tconnectsync options are
specified correctly, and that both t:connect and Nightscout are accessible:

```
https://YOUR-TCONNECTSYNC-APP-NAME.herokuapp.com/check_login?secret=YOUR_TCONNECTSYNC_HEROKU_SECRET_VALUE
```

If you experience any issues setting up tconnectsync with Heroku, you can do one of the following:
* Post in the **CGM in the Cloud** Facebook group
* Open a GitHub Issue at https://github.com/jwoglom/tconnectsync-heroku/issues/new

When asking for help, please be ready to copy-and-paste the output of the `check_login` URL
referenced above which contains diagnostic information which may help to solve your issue(s).

## Updating synchronization features

By default, tconnectsync-heroku will upload the following data from your pump to Nightscout:
* Basal events
* Bolus events

Tconnectsync supports additional so-called _synchronization features_ which enable it to send
additional pump data into Nightscout. [You can see a list of these features here](https://github.com/jwoglom/tconnectsync#What-Gets-Synced).

To set custom synchronization features, go into your Heroku Config Vars settings (Settings > Reveal Config Vars)
and add a key and value with the following:

* Key: `TCONNECTSYNC_HEROKU_FEATURES`
* Value: a comma-separated list of features, without spaces. e.g., `BASAL,BOLUS,PUMP_EVENTS`

If you don't set this value, tconnectsync-heroku will default to tconnectsync's default synchronization
features (only basal and bolus data).

## Updating to a new version

Updates are made frequently to tconnectsync to correct bugs or add new features.
When some time has past after setting up tconnectsync-heroku and you want to ensure
you are up to date, follow these instructions:

To update your Heroku instance of tconnectsync, perform the following steps.
This is a tconnectsync specific version of the "Deploy using Heroku Git"
instructions which are present in the "Deploy" tab of your Heroku console.

You should perform the following steps on a Linux or MacOS computer.
If using Windows, install the [Windows Subsystem for Linux](https://ubuntu.com/wsl) and
run these steps inside the Ubuntu Terminal.

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

## Alternate Configuration Using Background Tasks
What follows is an alternate option, which may be easier to set up but may not work for all setups:

Go into your Heroku Config Vars settings (Settings > Reveal Config Vars)
and add a key and value with the following:

* TCONNECTSYNC_HEROKU_INTERVAL_MINS - The interval at which a scheduled task should
  be performed for a synchronization. This will **only** function while the Flask
  application is running inside Heroku. (Heroku will occasionally shut down the app
  after some period of inactivity.)

For example:
* Key: `TCONNECTSYNC_HEROKU_INTERVAL_MINS`
* Value: `30`

When the Flask application is started, so long as it is running the tconnect
synchronization task will run at the given interval.

Note that **Heroku may shut down your dyno if it has not processed requests in
30 minutes**.

You should ideally set up UptimeRobot to ping your application at the index URL
(**not** the run endpoint, since that will cause the synchronization to happen
both triggered by UptimeRobot and the background task daemon itself).
This would reflect a URL such as:

```
https://YOUR-TCONNECTSYNC-APP-NAME.herokuapp.com/
```


[tconnectsync]: https://github.com/jwoglom/tconnectsync
[tconnect-installation]: https://github.com/jwoglom/tconnectsync#installation
[uptimerobot]: https://uptimerobot.com/
