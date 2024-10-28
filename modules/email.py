import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def send_otp(self, email, otp):
        msg = MIMEMultipart()
        msg["Subject"] = "Yupcha OTP"
        msg["From"] = "tuhin.paul.5tuhin@gmail.com"
        msg["To"] = email
        text = f"Hi, your otp is : {otp}"
        part = MIMEText(text, "plain")
        msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("tuhin.paul.5tuhin@gmail.com", "cpjb ncjz cmmc hrnc")
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()