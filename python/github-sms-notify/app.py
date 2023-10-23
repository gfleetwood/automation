from os import environ
from github import Github
from etext import send_sms_via_email

print("Running GitHub Notification Checks")

email = environ["GMAIL_ADDRESS"]
app_pw = environ["GMAIL_APP_PASSWORD"]
provider = environ["CELL_PROVIDER_PHONE_NUM"]
phone_number = environ["PHONE_NUM"]
g = Github(environ["GHUB"])

sender_credentials = (email, app_pw)
subject = "GitHub Notification"

usr = g.get_user()
notifications = ["{}: {}".format(note.repository.full_name, note.subject.title) for note in usr.get_notifications()]

_ = "No notifications" \
    if len(notifications) == 0 \
    else [
     send_sms_via_email(phone_number, note, provider, sender_credentials, subject = subject)
     for note in notifications
    ]
