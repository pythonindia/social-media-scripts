import base64
import sendgrid
import os
import csv
from sendgrid.helpers.mail import Email, Content, Mail, Attachment
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib

email_data = []
with open('attachment_data.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        email_data.append(row)

email_data.pop(0)

for data in email_data:
    email = data[0]
    filename = data[1]

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("contact@in.pycon.org")
    subject = "Subject for attachment email"
    to_email = Email(email)
    content = Content("text/html", "Hi,<br>Please find attached the documents for PyCon India.")

    file_path = filename
    with open(file_path,'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.content = encoded
    attachment.type = "application/pdf"
    attachment.filename = filename
    attachment.disposition = "attachment"
    attachment.content_id = "Attachment email"

    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print("Sent email to {0}".format(email))
    except urllib.HTTPError as e:
        print(e.read())
        exit()

# print(response.status_code)
# print(response.body)
# print(response.headers)