from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class EmailSchema(BaseModel):
    name : str
    email :str
    subject: str
    message: str


def send_email_background(email_data: EmailSchema):
    sender_email = "kalkeeshjamipics@gmail.com"  
    receiver_email = "kalkeeshjami@gmail.com"  
    sender_password = "nqkc gdos ngdx hvuj"  

    message = MIMEMultipart("alternative")
    message["Subject"] = email_data.subject
    message["From"] = sender_email
    message["To"] = receiver_email    
    text = email_data.message
    html = f"<html><body><p> Hi I am {email_data.name}, my mail is {email_data.email} </p><br><p>{email_data.message}</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        # print(f"Email sent from {sender_email} to {receiver_email}")
    except Exception as e:
        # print(f"Error sending email: {str(e)}")
        pass

@app.post("/send-email/")
async def send_email(email_data: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_background, email_data)
    return {"message": f"Email is being sent"}
@app.get("/")
async def checkk():
    return {"status":"successfull"}
