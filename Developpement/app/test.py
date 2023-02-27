import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 
 
message = Mail(
from_email="bdboum45@gmail.com",
to_emails="luis.doudeau@gmail.com",
subject='Invitation au festival bdBOUM ' + "2023", # a changé
html_content='<strong>and easy to do anywhere, even with Python</strong>',
)
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)