# %% codecell
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import sched, time

# %% codecell
end = dt.datetime.now()
start = end - dt.timedelta(days=180)
df = web.DataReader('TECK', 'yahoo', start, end)
df

# Creating a scheduler to send an email everyday
scheduler = sched.scheduler(time.time, time.sleep)

# Create a function to get the stock data from yahoo and send email with the plot
def send_email(sc):

    # Get the stocks data from yahoo
    end = dt.datetime.now()
    start = end - dt.timedelta(days=180)
    df = web.DataReader('TECK', 'yahoo', start, end)
    df

    # Create a plot from the stocks data
    style.use('bmh')
    f, ax = plt.subplots(1, 1, figsize=(10, 7))
    df[['High', 'Low']].plot(ax=ax)
    plt.xticks(rotation=90)
    plt.ylabel('US Dollars')
    plt.title('Teck Resources Limited')
    f.savefig("TECK")

    # Send email with the image attachment
    msg = MIMEMultipart()
    body = "Thank you for using my Python code"
    msg.attach(MIMEText(body,'plain'))
    img_data = open('TECK.png', 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename('TECK.png'))
    msg.attach(image)

    ## Created environmental variables to hide my username and password
    #username = os.environ.get('GMAIL_USERNAME')
    #password = os.environ.get('GMAIL_PASSWORD')
    ## For this to work, you need to setup https://myaccount.google.com/lesssecureapps to ON
    username = 'abuadilah1429@gmail.com'
    password = 'msqpdo63'

    msg['From'] = 'abuadilah1429@gmail.com'
    msg['To'] = 'abuadilah1429@gmail.com'
    msg['subject'] = 'Teck Resources Limited - Stock Prices'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    print ("Email Sent")
    scheduler.enter(10, 1, send_email, (sc,))

# Send the email everyday
scheduler.enter(10, 1, send_email, (scheduler,))
scheduler.run()
