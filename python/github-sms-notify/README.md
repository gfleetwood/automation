# GitHub SMS Notifications

## Overview

A simple script to text you the repo's name and subject title when you have unread GitHub notifications. It runs through GitHub Actions. A previous iteration used Twilio, but apparently you can send texts through email. That simplifies things so you don't have to pay for a Twilio phone number. This implementation depends heavily on the etext library:

https://github.com/AlfredoSequeida/etext

Follow the instructions here to get an app password for Gmail:

https://myaccount.google.com/apppasswords

You need the following environment variables locally:

* GMAIL_ADDRESS
* GMAIL_APP_PASSWORD
* CELL_PROVIDER_PHONE_NUM
* PHONE_NUM
* GHUB

Look up the CELL_PROVIDER_PHONE_NUM here:

https://github.com/AlfredoSequeida/etext/blob/main/etext/providers.py

For GitHub Actions you also need to set them in GitHub: 

https://damienaicheh.github.io/github/actions/2021/04/15/environment-variables-secrets-github-actions-en.html

The GitHub Action should run smoothly.
