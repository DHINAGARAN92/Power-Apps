// pip install secure-smtplib

import smtplib
from email.message import EmailMessage

# Input: recipient email ID
to_email = input("Enter recipient email ID: ")

# Your Microsoft 365 credentials
EMAIL_ADDRESS = 'your_email@yourdomain.com'
EMAIL_PASSWORD = 'your_app_password'  # App Password if MFA is on

# Create the email message
msg = EmailMessage()
msg['Subject'] = 'Hello from Python!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = to_email
msg.set_content('This is a test email sent using Microsoft 365 SMTP via Python.')

try:
    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Email sent successfully to", to_email)
except Exception as e:
    print("Failed to send email:", e)
