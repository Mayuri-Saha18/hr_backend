from fastapi import APIRouter, HTTPException, Request
from modules.authentication_db import Database
from pydantic import BaseModel
import random
from modules.utils import is_cookie_expired

router = APIRouter()
database = Database()

COOKIE_NAME = "sessions"

@router.on_event("startup")
async def on_startup():
    await database.initialize()

def generate_id():
    id = random.randint(100000, 999999)
    return id
    

@router.post("/profile_data")
async def application_data(request:Request):
    try:
        data = await request.json()
        cookie_id = request.cookies['session']
        if cookie_id:
            # if await is_cookie_expired(cookie_id):
            #     return {"detail": "Cookie expired"}
            # else:
                # print("Here")
            await database.save_user(data['fname'], data['lname'], data['phone'], data['email'])
            return{"success": True, "Message" : "Userdata Saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# @router.post("/profile_data")
# async def application_data(request:Request, user_data: UserData):
#     try:
#         cookie_id = request.cookies.get(COOKIE_NAME)
#         if cookie_id:
#             if await is_cookie_expired(cookie_id):
#                 return {"detail": "Cookie expired"}
#         else:
#             await database.save_user(user_data.name, user_data.phone, user_data.email, user_data.address)
#         return{"Message" : "Userdata Saved"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))