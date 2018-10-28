# PyCon Emailer

PyCon emailer contains a bunch of scripts that are useful for sending bulk emails to participants as and when required. You just need to get the data dump in csv files and make small changes in the scripts to read the data from files and send the emails.

The emailer has 2 scripts one for sending emails with attachements [attachment_emailer.py](attachment_emailer.py) and other uses a sengrid transactional template for sending bulk emails [emailer.py](emailer.py)

## Setup and Usage

The scripts uses sendgrid python api to send emails. To use the script first signup on [sendgrid](https://app.sendgrid.com) and get an API key. Then follow the following steps

1. Create a `sendgrid.env` file and export the api key there. You can simply use this commands

```
echo "export SENDGRID_API_KEY='YOUR_SENGRID_API_KEY'" > sendgrid.env
```

2. Next add the csv data in relevant csv files. In case you have some differnt data you can change the scripts to read the appropriate keys.

3. Run the sengrid.env file using `source sendgrid.env` to export the API key

5. Install dependencies using `pip install requirements.txt`

4. Run the scripts and the emails will be sent with the log printed in the terminal

