from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from modules.utils import is_cookie_expired
from modules.authentication_db import Database

router = APIRouter()
database = Database()


class EditUserData(BaseModel):
    id: str
    name: str
    phone: str
    address: str




COOKIE_NAME = "session"


@router.on_event("startup")
async def on_startup():
    await database.initialize()


@router.get("/get_all_users")
async def get_user_data(request: Request):
    cookie_id = request.cookies.get(COOKIE_NAME)
    if cookie_id:
        if await is_cookie_expired(cookie_id):
            return {"detail": "Cookie expired"}
        else:
            result = await database.user_data_from_db()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/get_user_data")
async def edit_user_data(request: Request, user: EditUserData):
    cookie_id = request.cookies.get(COOKIE_NAME)
    if cookie_id:
        if await is_cookie_expired(cookie_id):
            return {"detail": "Cookie expired"}
        else:
            result = await database.edit_user_data(
                user.id, user.name, user.phone, user.address
            )
            print(result)
            if result:
                return {
                    "message": f"User data updated successfully for user : {user.email}"
                }
            else:
                raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# @router.get("/get_user")
# async def get_user(request: Request):
#     try:
#         cookie_id = request.cookies.get(COOKIE_NAME)
#         if cookie_id:
#             user_id = cookie_id.split("_")[0]
#             if user_id:
#                 user = await database.get_user(int(user_id))
#                 jobs_applied = await database.get_jobs_applied(int(user_id))
#                 jobData = []
#                 for job in jobs_applied:
#                     job_info = {
#                         "job_id": job['job_id'],
#                         "application_status": job['application_status'],
#                         "hr_status": job['hr_status']
#                     }
#                     jobData.append(job_info)
#                 data = {
#                     "user_id": user["user_id"],
#                     "fname": user["first_name"],
#                     "lname": user["last_name"],
#                     "phone": user["phone"],
#                     "email": user["email"],
#                     "jobs_applied": jobData
#                 }
#                 return {"status_code": 200, "success": True, "data": data}
#             else:
#                 return HTTPException(status_code=400, detail="User not found")
#         else:
#             return HTTPException(status_code=401, detail="Unauthorized")
#     except Exception:
#         return HTTPException(status_code=500, detail="Internal Server Error")
