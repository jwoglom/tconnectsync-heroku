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
**Start by clicking the Deploy button below:**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jwoglom/tconnectsync-heroku)

For *App name*, you can enter any value. 
We recommend **`MyNightscoutSite-tconnect`**.

The app name determines the URL to access your tconnectsync-heroku website, e.g. if you enter the app name `MyNightscoutSite-tconnect`, then the URL for tconnectsync-heroku will be `https://MyNightscoutSite-tconnect.herokuapp.com`.

The remainder of the options are [tconnectsync environment variables][tconnect-installation]:

* `TCONNECT_EMAIL` - Your t:connect email
* `TCONNECT_PASSWORD` - Your t:connect password
* `NS_URL` - Your Nightscout site URL (e.g. https://yournightscoutsite.herokuapp.com)
* `NS_SECRET` - Your Nightscout `API_SECRET` value
* `PUMP_SERIAL_NUMBER` - The numeric serial number of your pump. Enter only the number, do not include '#'
* `TIMEZONE_NAME` - The timezone code in which your phone and pump's time is set. ([View a full list of valid values](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))

A new variable called `TCONNECTSYNC_HEROKU_SECRET` will be automatically generated for you.
This secret password will be used to access API endpoints which trigger your pump data from tconnect
to be synchronized to Nightscout, as well as view the current status of synchronization.
(You can think of it like the tconnectsync equivalent to Nightscout's `API_SECRET`.)
You can find its automatically generated value by going to Settings > Reveal Config Vars in your Heroku dashboard after setup.

Once you've filled out the Create New App form and pressed *Deploy App*, you'll be taken to the Heroku dashboard.
From here, you can click on **Open App** to see whether the tconnectsync-heroku server is running.

<img src="https://i.imgur.com/ND0jouy.png" width="600" />

If you see a page like the following, then you're ready to move on!

<img src="https://i.imgur.com/1HSN6nn.png" width="600" />

If you get an error, then jump to the instructions in the **Testing** section below.

Otherwise, continue reading below to set up tconnectsync-heroku by creating an account with a separate service, **UptimeRobot**.

## UptimeRobot

Even though your Heroku app is already up and running, we need to set up a service called **UptimeRobot**
which will send a request to your Heroku app to keep it alive so that it can continue to process
your incoming t:connect data in the background.

### Creating an Account
Create an account at [UptimeRobot][uptimerobot] by going to https://uptimerobot.com.

<img src="https://i.imgur.com/ZiTPK9H.png" width="500" />

<img src="https://i.imgur.com/ygTzmyY.png" width="500" />

Once you register, you will be prompted to verify your email address.
Click the link you receive from UptimeRobot in your email.

<img src="https://i.imgur.com/SuRy9Ex.png" width="500" />

If you're asked to upgrade to the PRO plan, click **Maybe later**

<img src="https://i.imgur.com/zNBZafz.png" width="500" />

### Setting Up UptimeRobot
Now that you have an account and are logged in, you should see a page like the following:

<img src="https://i.imgur.com/FNeEWJX.png" width="900" />

Click the **Add New Monitor** button. You'll see a popup like this:

<img src="https://i.imgur.com/RJfW9wB.png" width="500" />

Enter the following, one at a time:

* Monitor Type: **HTTP(s)**
* Friendly Name: **tconnectsync**
* Monitoring Interval: **every 30 minutes**
* Monitor Timeout: **1 minute**

Enter the following as the URL:
```
https://MyNightscoutSite-tconnect.herokuapp.com/run?secret=YOUR_TCONNECTSYNC_HEROKU_SECRET_VALUE
```

**MyNightscoutSite-tconnect** is the App Name you provided for tconnectsync-heroku.

To get the value of **YOUR_TCONNECTSYNC_HEROKU_SECRET_VALUE**:

* Go into your Heroku dashboard (https://dashboard.heroku.com) and select the app you created for tconnectsync:

<img src="https://i.imgur.com/SKPcBCw.png" width="500" />

* Click on Settings > Reveal Config Vars.

<img src="https://i.imgur.com/u6z9Kph.png" width="500" />

* Now find the row which has `TCONNECTSYNC_HEROKU_SECRET` displayed on the left,
  and copy the value contained in the right-most text box next to it.
  This is the value of the `TCONNECTSYNC_HEROKU_SECRET` environment variable.

(If you'd like, you can change the value here to a different password.
If so, then save settings and then restart the app in heroku via More > Restart All Dynos.)


Your options should look similar to this (but with your actual tconnectsync-heroku URL and secret value):

<img src="https://i.imgur.com/wJ7DfqT.png" width="900" />

Click **Create Monitor**.
Now, every 30 minutes, tconnectsync will be triggered to synchronize your data between t:connect and Nightscout!

## Testing

You can hit the following URL to verify that your tconnectsync options are
specified correctly, and that both t:connect and Nightscout are accessible:

```
https://MyNightscoutSite-tconnect.herokuapp.com/check_login?secret=YOUR_TCONNECTSYNC_HEROKU_SECRET_VALUE
```

(Remember to replace `MyNightscoutSite-tconnect` and `YOUR_TCONNECTSYNC_HEROKU_SECRET_VALUE` with your own values like mentioned before.)

There is a lot of debugging output on this page, so scroll to the very bottom.
If it says **No API errors returned!** then you are all good to go!

If the page doesn't load, you can also view the application-side error logs by going to the Heroku dashboard and clicking on **More > View logs**:

<img src="https://i.imgur.com/JzMagmv.png" width="500" />

**If you need help,** you can do one of the following:
* Post in the **CGM in the Cloud** Facebook group
* Open a GitHub Issue at https://github.com/jwoglom/tconnectsync-heroku/issues/new

When asking for help, please be ready to copy-and-paste the output of the `check_login` URL
referenced above which contains diagnostic information which may help to solve your issue(s).

**The remainder of the instructions below are for advanced use cases.**
Once you've gotten to this point, wait 30 minutes to see if pump data starts appearing in Nightscout!

## Troubleshooting

### _I get a Heroku error page when clicking **Open App** from the Heroku dashboard_

View the application-side error logs by going to the Heroku dashboard and clicking on **More > View logs**:

<img src="https://i.imgur.com/JzMagmv.png" width="500" />

Check if there are any errors about invalid configuration options.
If the problem is something else, follow the **If you need help** instructions above.

### _The `check_login` page gives a `Received ApiException in ControlIQApi: ControlIQ API HTTP 404 response` error_

Please verify that you've completed the following steps:

* Have you created an account on the tconnect website?
* With the tconnect credentials you've specified, can you:
  * Log in to the Android or iOS app, with your pump paired and sending data
  * Log in at https://tconnect.tandemdiabetes.com and see your pump information appear

If tconnectsync still gives this error, try:

* Downloading the [Windows or MacOS TConnect Uploader application](https://tconnect.tandemdiabetes.com/GettingStarted/Download.aspx) and plug your pump into your computer to upload your settings.
* Resetting your password at https://tconnect.tandemdiabetes.com and setting it to the same password you use in the Android or iOS app

If this doesn't help, follow the **If you need help** instructions above.

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
