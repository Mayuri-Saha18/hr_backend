from fastapi import APIRouter, HTTPException, Response
from modules.authentication_db import Database
from pydantic import BaseModel
import  uuid
import random
from datetime import datetime, timedelta

router = APIRouter()

database = Database()

@router.on_event("startup")
async def on_startup():
    await database.initialize()

class VerifyOtpData(BaseModel):
    email: str
    otp: str


COOKIE_NAME = "session"
           
def generate_id():
    id = random.randint(100000, 999999)
    return id

async def generate_cookie_id(user_exists, email):
    if len(user_exists) > 0:
        print("user exsists")
        id = user_exists[0]['user_id']
        cookie_id = f"{id}_{str(uuid.uuid4())}"
        await database.insert_session(email, cookie_id, id)
        return False, cookie_id
    else:
        print("new user")
        id = generate_id()
        cookie_id = f"{id}_{str(uuid.uuid4())}"
        await database.insert_session(email, cookie_id, id)
        return True, cookie_id
        

@router.post("/verify_otp")
async def verify_otp(data: VerifyOtpData, response: Response):
    otp_is_expired = await database.check_otp(data.email)
    if otp_is_expired:
        return {"success": False, "message": "OTP expired"}
    else:
        otp = await database.get_otp(data.email)
        if otp == data.otp:
            res = await database.check_user(data.email)
            new_user, cookie_value = await generate_cookie_id(res["data"], data.email)
            # expiry_time = datetime.now() + timedelta(seconds=300)
            # exp_unix = int(expiry_time.timestamp())
            response.set_cookie(
                key=COOKIE_NAME,
                value=cookie_value,
                max_age=60 * 60, # 5 minutes
                httponly=True,
                samesite="lax",
                domain="localhost"
            )
            await database.remove_otp_record(data.email)
            if new_user: 
                return {"success": True, "message": "OTP verified successfully." , "new_user": True}
            else:
                return {"success": True, "message": "User Exists", "new_user": False}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP.")