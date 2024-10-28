from fastapi import APIRouter, HTTPException, Depends, Request, Response
from modules.form_db import FormDB
from modules.email import EmailService
import random, uuid
from datetime import datetime, timedelta
from dependencies import initializeFormDb


form_router = APIRouter()
email_service = EmailService()
COOKIE_NAME = "session"


def generate_id():
    id = random.randint(100000, 999999)
    return id


# @form_router.post("/get_job")
# async def submit_form(request: Request, formDb: FormDB = Depends(initializeFormDb)):
#     try:
#         data = await request.json()
#         print(data)
#         # created = datetime.now()
#         # modified = datetime.now()
#         # email = data["Personal"]['email']

#         # await JobsAppliedHelper(data["Declaration"], email, formDb, created, modified)
#         return {"status_code": 200, "success": True}
#     except Exception as e:
#         return HTTPException(status_code=500, detail=str(e))

