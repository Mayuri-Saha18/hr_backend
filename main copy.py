from fastapi import FastAPI, HTTPException, Response, Request, BackgroundTasks, Cookie, Header
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import asyncpg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import uvicorn
import asyncio
from datetime import datetime, timedelta
import logging
import uuid


app = FastAPI()

COOKIE_NAME = "session"

# Configure session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="1234",
    max_age=10,  # 5 minutes in seconds
)

class EmailData(BaseModel):
    name: str
    phone: str
    email: str

class VerifyOtpData(BaseModel):
    email: str
    otp: str

class LoginData(BaseModel):
    email: str

def generate_otp():
    otp = random.randint(1000, 9999)
    return otp

def send_otp_email(email, otp):
    msg = MIMEMultipart()
    msg["Subject"] = "Yupcha OTP"
    msg["From"] = "tuhin.paul.5tuhin@gmail.com"
    msg["To"] = email
    text = f"Hi, your otp is : {otp}"
    part = MIMEText(text, "plain")
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("tuhin.paul.5tuhin@gmail.com", "gyog yeek ilow stka")
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

async def delete_otp(email):
    await asyncio.sleep(300)  # DELETS otp after 5 minutes
    async with asyncpg.create_pool(
        user="postgres", database="career", host="localhost"
    ) as pool:
        async with pool.acquire() as connection:
            await connection.execute(
                """
                UPDATE login SET otp = NULL WHERE email = $1
                """,
                email,
            )

@app.post("/send_otp")
async def send_otp(email_data: EmailData, background_tasks: BackgroundTasks):
    otp = str(generate_otp())
    try:
        send_otp_email(email_data.email, otp)
        async with asyncpg.create_pool(
            user="postgres", database="career", host="localhost"
        ) as pool:
            async with pool.acquire() as connection:
                await connection.execute(
                    """
                    DELETE FROM login WHERE email = $1
                    """,
                    email_data.email,
                )
                await connection.execute(
                    """
                    INSERT INTO login (name, phone, email, otp)
                    VALUES ($1, $2, $3, $4)
                    """,
                    email_data.name,
                    email_data.phone,
                    email_data.email,
                    str(otp),
                )
        background_tasks.add_task(delete_otp, email_data.email)
        return {"message": "OTP sent to your email."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify_otp")
async def verify_otp(data: VerifyOtpData, response: Response):
    async with asyncpg.create_pool(
        user="postgres", database="career", host="localhost"
    ) as pool:
        async with pool.acquire() as connection:
            result = await connection.fetchval(
                """
                SELECT otp FROM login WHERE email = $1
                """,
                data.email,
            )
            if result and result == data.otp:
                COOKIE_ID = data.email+str(uuid.uuid4())
                seconds = 10
                EXPIRY_TIME =datetime.now() + timedelta(seconds)

                # Save the cookie and expiry time in the database
                await connection.execute(
                    """
                    INSERT INTO session (email, session, expiry)
                    VALUES ($1, $2, $3)
                    """,
                    data.email,
                    COOKIE_ID,
                    EXPIRY_TIME,
                )
                # Set a session variable indicating successful verification
                response.set_cookie(
                    key=COOKIE_NAME,
                    value=COOKIE_ID,
                    max_age=seconds,  # 5 minutes
                    httponly=True,
                    samesite="lax",
                )
                # Delete the OTP from the database after successful verification
                await connection.execute(
                    """
                    UPDATE login SET otp = NULL WHERE email = $1
                    """,
                    data.email,
                )
                return {"message": "OTP verified successfully."}
            else:
                raise HTTPException(status_code=400, detail="Invalid OTP.")

async def is_cookie_expired(cookie_id: str) -> bool:
    async with asyncpg.create_pool(
        user="postgres", database="career", host="localhost"
    ) as pool:
        async with pool.acquire() as connection:
            result = await connection.fetchrow(
                """
                SELECT expiry FROM session WHERE session = $1
                """,
                cookie_id,
            )
            if result:
                expiry_time = result[0]
                return datetime.now() + timedelta() > expiry_time
            else:
                return True


@app.get("/get_user_data")
async def get_user_data(request: Request):
    cookie_id = request.cookies.get(COOKIE_NAME)
    if cookie_id:
        if await is_cookie_expired(cookie_id):
            return {"detail": "Cookie expired"}
        else:
            # Proceed with fetching user data
            async with asyncpg.create_pool(
                user="postgres", database="career", host="localhost"
            ) as pool:
                async with pool.acquire() as connection:
                    result = await connection.fetchrow(
                        """
                        SELECT * FROM login
                        """
                    )
                    logging.info(f"Query result: {result}")
                    if result:
                        return {"name": result[0], "phone": result[1], "email": result[2], "session": cookie_id}
                    else:
                        raise HTTPException(status_code=404, detail="User not found.")
    else:
        return {"detail": "Cookie not found in request."}
    
from typing import Optional
@app.get("/items")
async def get_items(
    cookie_id: Optional[str] = Cookie(None), 
    accept_encoding: Optional[str] = Header(None),
    sec_ch_ua: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
):
    return{
        "cookie_id": cookie_id,
        "accept_encoding": accept_encoding,
        "sec_ch_ua": sec_ch_ua,
        "user_agent": user_agent
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
