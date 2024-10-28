import json, time
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from modules.authentication_db import AuthenticationDB
from modules.email import EmailService
from pydantic import BaseModel
import random, uuid
from dependencies import initializeAuthDb

auth_router = APIRouter()
email_service = EmailService()
COOKIE_NAME = "session"


class LoginData(BaseModel):
    email: str

class OtpData(BaseModel):
    email: str
    otp: int

class ProfileData(BaseModel):
    email: str
    fname: str
    lname: str
    phone: str

class SavedData(BaseModel):
    email: str
    job_id: int

def generate_otp():
    otp = random.randint(1000, 9999)
    return otp


def generate_id():
    id = random.randint(100000, 999999)
    return id


async def generate_cookie_id(user_exists, email, db):
    if len(user_exists) > 0:
        print("user exsists")
        id = user_exists[0]["user_id"]
        cookie_id = f"{id}_{str(uuid.uuid4())}"
        await db.insert_session(email, cookie_id, id)
        return False, cookie_id, id
    else:
        print("new user")
        id = generate_id()
        cookie_id = f"{id}_{str(uuid.uuid4())}"
        await db.insert_session(email, cookie_id, id)
        return True, cookie_id, id


@auth_router.post("/login")
async def login(
    request: Request, data: LoginData, auth_db: AuthenticationDB = Depends(initializeAuthDb)
):
    otp = int(generate_otp())
    data = json.loads(data.json())
    try:
        email_service.send_otp(data["email"], otp)
        await auth_db.delete_otp(data["email"])
        await auth_db.insert_otp(data["email"], otp)
        return {"success": True, "message": "OTP sent to your email."}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@auth_router.post("/verify_otp")
async def verify_otp(data: OtpData, request: Request,
    response: Response,
    auth_db: AuthenticationDB = Depends(initializeAuthDb)):
    try:
        data = json.loads(data.json())
        otp_is_expired = await auth_db.check_otp(data["email"])
        if otp_is_expired:
            return {"success": False, "message": "OTP expired"}
        else:
            otp = await auth_db.get_otp(data["email"])
            if otp == int(data["otp"]):
                res = await auth_db.check_user(data["email"])
                new_user, cookie_value, id = await generate_cookie_id(
                    res["data"], data["email"], auth_db
                )
                response.set_cookie(
                    key=COOKIE_NAME,
                    value=cookie_value,
                    max_age=60 * 60 * 24 * 7,  # 7 days
                    expires=time.time() + 50000000000,  # 7 days
                    httponly=True,
                    samesite="none",
                    domain="localhost",
                    secure=True,
                )
                await auth_db.remove_otp_record(data["email"])
                if new_user:
                    return {
                        "success": True,
                        "message": "OTP verified successfully.",
                        "new_user": True,
                        "sl": id,
                    }
                else:
                    return {
                        "success": True,
                        "message": "User Exists",
                        "new_user": False,
                        "sl": id,
                    }
            else:
                raise HTTPException(status_code=400, detail="Invalid OTP")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@auth_router.post("/profile_data")
async def application_data(
    data: ProfileData, request: Request, auth_db: AuthenticationDB = Depends(initializeAuthDb)
):
    try:
        data = await request.json()
        cookie_id = request.cookies["session"]
        if cookie_id:
            # if await is_cookie_expired(cookie_id):
            #     return {"detail": "Cookie expired"}
            # else:
            # print("Here")
            await auth_db.save_user(
                data["fname"], data["lname"], data["phone"], data["email"]
            )
            return {"success": True, "Message": "Userdata Saved"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@auth_router.get("/get_user")
async def get_user(
    request: Request, auth_db: AuthenticationDB = Depends(initializeAuthDb)
):
    try:
        cookie_id = request.cookies.get(COOKIE_NAME)
        if cookie_id:
            user_id = cookie_id.split("_")[0]
            if user_id:
                user = await auth_db.get_user(int(user_id))
                jobs_applied = await auth_db.get_jobs_applied(int(user_id))
                saved_jobs = await auth_db.get_saved_jobs(int(user_id))
                applied_jobData = []
                saved_jobData = []
                for job in jobs_applied:
                    job_info = {
                        "job_id": job["job_id"],
                        "job_title": job["job_title"],
                        "application_status": job["application_status"],
                    }
                    applied_jobData.append(job_info)

                for saved in saved_jobs:
                    saved_info = {
                        "job_id": saved["job_id"],
                        "job_title": saved["job_title"],
                        "job_name": saved["job_name"],
                    }
                    saved_jobData.append(saved_info)

                data = {
                    "user_id": user["user_id"],
                    "fname": user["first_name"],
                    "lname": user["last_name"],
                    "phone": user["phone"],
                    "email": user["email"],
                    "jobs_applied": applied_jobData,
                    "saved_jobs": saved_jobData,
                }
                return {"status_code": 200, "success": True, "data": data}
            else:
                return HTTPException(status_code=400, detail="User not found")
        else:
            return HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@auth_router.post("/logout")
async def logout(
    response: Response,
    request: Request,
    auth_db: AuthenticationDB = Depends(initializeAuthDb),
):
    print(response)
    try:
        
        cookie_id = request.cookies.get(COOKIE_NAME)

        if cookie_id:
            
            user_id = cookie_id.split("_")[0]
            user = await auth_db.get_user_by_id(int(user_id))

            if not user:
                return HTTPException(status_code=404, detail="User not found.") 
            
            await auth_db.delete_session(int(user_id))
            response.delete_cookie(COOKIE_NAME, domain="localhost")
            return {"success": True, "message": "Successfully logged out."}

        else:
            
            return HTTPException(status_code=401, detail="No active session found.")

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
@auth_router.post("/save_job")
async def save_job(
    data: SavedData, request: Request, auth_db: AuthenticationDB = Depends(initializeAuthDb)
):
    data = json.loads(data.json())
    print(data)
    try:
       
        cookie_id = request.cookies.get(COOKIE_NAME)
        print(cookie_id)
        if cookie_id:
            user_id = cookie_id.split("_")[0]
            if user_id:
                job_id = data["job_id"] 
                # Check if the job is already saved
                is_saved = await auth_db.is_job_saved(int(user_id), job_id)
                if is_saved:
                    # If job is already saved, remove it (un-save action)
                    await auth_db.remove_saved_job(int(user_id), job_id)
                else:
                    # If job is not saved, add it to saved jobs
                    await auth_db.save_job(int(user_id), job_id)
                return {"status_code": 200, "success": True, "message": "Job saved status toggled."}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @auth_router.post("/update_user")
# async def edit_user_data(request: Request, auth_db: AuthenticationDB = Depends(initializeAuthDb)):
#     try:
#         data = await request.json()
#         cookie_id = request.cookies.get(COOKIE_NAME)
#         if cookie_id:
#             # if await is_cookie_expired(cookie_id):
#             #     return {"detail": "Cookie expired"}
#             # else:
#             result = await auth_router.edit_user_data(
#                 user.id, user.name, user.phone, user.address
#             )
#             print(result)
#             if result:
#                 return {
#                     "message": f"User data updated successfully for user : {user.email}"
#                 }
#             else:
#                 raise HTTPException(status_code=404, detail="User not found.")
#         else:
#             raise HTTPException(status_code=401, detail="Unauthorized")

#     except Exception as e:
#         return HTTPException(status_code=500, detail=str(e))
