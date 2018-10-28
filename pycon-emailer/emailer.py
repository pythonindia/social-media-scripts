import sendgrid
import os
import csv
from sendgrid.helpers.mail import *

proposals = []
with open('proposal_data.csv', 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        proposals.append(row)

proposals.pop(0)

for i, proposal in enumerate(proposals):
    email = proposal[0]
    name = proposal[1]
    proposal_name = proposal[2]

    mail = Mail()
    mail.from_email = Email('contact@in.pycon.org')
    mail.template_id = 'd-123abc'
    p = Personalization()
    p.add_to(Email(email))
    p.dynamic_template_data = {
        'name': name,
        'proposal': proposal_name
    }
    mail.add_personalization(p)

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.mail.send.post(request_body=mail.get())
    print(i, 'Sent email to {0} for proposal {1}'.format(email, proposal_name))
    # print(response.status_code)
    # print(response.headers)
    # print(response.body)
