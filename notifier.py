from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from terminal_msg import *

import csv
import os
import smtplib


def get_users_emails(csv_file: str):
    '''
    description:
        get users email addresses from the csv file.
        returns False if file is missing else returns
        list of user email addresses.

    params:
        csv_file (str): csv file path

    returns: 
        list | False
    '''
    # check if file exists
    if not os.path.exists(csv_file):
        warn(f"{csv_file} csv file is missing.")
        return False

    # extract user email addresses from the csv file
    emails = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        next(reader)    # skip header
        for name, email in reader:
            emails.append(email.strip())

    return emails


def notifications_to_html(notifications: list[list]):
    '''
    description:
        format notifications list into html code.

    params:
        notifications (list): list of notifications [[link,name]]

    returns: 
        str
    '''
    html_text = ''
    def html_formatter(
        link, name): return f'<a href="{link}">{name.capitalize()}</a><br>'
    for notification in notifications:
        link, name = notification
        html_text += html_formatter(link, name)

    return html_text


def send_html_email(sender_email: str, sender_passwd: str, receiver_emails: list[str], plain_text: str, html_text: str):
    '''
    description:
        sends html email to the users.

    params:
        sender_email (str): gmail sender email
        sender_passwd (str): gmail sender app password
        receiver_emails (list): list of receiver email addresses as str
        plain_text (str): plain text in email
        html_text (str): html text in email 

    returns: 
        bool
    '''
    message = MIMEMultipart("alternative")
    message["Subject"] = "Govt. Scheme Notifier!!"
    message["From"] = sender_email
    message["To"] = sender_email

    message.attach(MIMEText(plain_text, 'plain'))
    message.attach(MIMEText(html_text, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_passwd)
        server.sendmail(sender_email, receiver_emails, message.as_string())
        server.quit()
        return True
    except Exception as e:
        error(e)
        return False


def notify_users(csv_file: str, notifications: list, sender_email: str = None, sender_passwd=None):
    '''
    description:
        sends notification email to the users.

    params:
        csv_file (str): csv file path
        notifications (list): notification in [[link(str), Title(str)]] format
        sender_email (str): gmail sender email
        sender_passwd (Str): gmail sender app password

    returns: 
        bool
    '''
    status = False
    emails = get_users_emails(csv_file)

    if emails is False:
        error("emails file not found found.")
        exit(2)

    html_text = '<strong>Latest Schemes</strong><br><br>'
    html_text += notifications_to_html(notifications)

    if send_html_email(sender_email, sender_passwd, emails, 'Notifier!!', html_text):
        success("Emails sent successfully.")
        status = True
    else:
        warn("Emails were not sent.")

    return status
