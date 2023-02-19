import smtplib
import requests
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from dotenv import load_dotenv, find_dotenv
import os, io

def getTodaysImages(contests):
    images = []
    for contest in contests:
        generatedImage = requests.post("http://127.0.0.1:5000/download", json=contest).content
        images.append(generatedImage)
    return images

def mailContests(send_from, send_to, images):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()

    load_dotenv(find_dotenv())
    # generate from your accounts.google.com -> security -> app passwords
    smtp.login(send_from, os.environ.get("CONTESTSCRAPERPASSWORD"))

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Contest Details For Instagram Story"

    msg.attach(MIMEText("Find attachments"))

    for i, image in enumerate(images):
        part = MIMEApplication(
            image,
            Name='contest' + str(i) + '.jpeg'
        )
        part['Content-Disposition'] = 'attachment; filename=contest' + \
            str(i) + '.jpeg'
        msg.attach(part)
    
    smtp.sendmail(send_from, send_to, msg.as_string())


todays_contests = requests.get("http://127.0.0.1:5000/allcontests")
todays_images = getTodaysImages(todays_contests.json())

# use turinghut.vnrvjiet.in mail once it's activated
mailContests('khssupriya@gmail.com', ['khssupriya@gmail.com'], todays_images)
