from fastapi import APIRouter, HTTPException, Depends, Request, Response
from modules.form_db import FormDB
from modules.email import EmailService
import random, uuid
from datetime import datetime, timedelta
from dependencies import initializeFormDb
from modules.submitHelper import EducationSubmitHelper, PersonalSubmitHelper, ProfessionalSubmitHelper, DeclarationSubmitHelper, JobsAppliedSubmitHelper
from modules.fetchHelper import PersonalFetchHelper, EducationFetchHelper, ProfessionalFetchHelper, DeclarationFetchHelper

form_router = APIRouter()
email_service = EmailService()
COOKIE_NAME = "session"


def generate_id():
    id = random.randint(100000, 999999)
    return id


@form_router.post("/submit")
async def submit_form(request: Request, formDb: FormDB = Depends(initializeFormDb)):
    try:
        data = await request.json()
        created = datetime.now()
        modified = datetime.now()
        email = data["Personal"]['email']
        await PersonalSubmitHelper(data["Personal"], formDb, created, modified)
        await EducationSubmitHelper(data["Education"], formDb, created, modified)
        await ProfessionalSubmitHelper(data["Professional"], formDb, created, modified)
        await DeclarationSubmitHelper(data["Declaration"], formDb, created, modified)
        await JobsAppliedSubmitHelper(data["Declaration"], email, formDb, created, modified)
        return {"status_code": 200, "success": True}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    
    
@form_router.get("/fetch")
async def fetch_data(which: str, request: Request, formDb: FormDB = Depends(initializeFormDb)):
    try:
        cookie_id = request.cookies.get(COOKIE_NAME)
        if cookie_id:
            user_id = cookie_id.split("_")[0]
            if user_id:
                if which == 'personal':
                    data = await PersonalFetchHelper(formDb, user_id)
                    return {"status_code": 200, "success": True, "data": data}
                if which == 'education':
                    data = await EducationFetchHelper(formDb, user_id)
                    return {"status_code": 200, "success": True, "data": data}
                if which == 'professional':
                    data = await ProfessionalFetchHelper(formDb, user_id)
                    return {"status_code": 200, "success": True, "data": data}
                if which == 'decleration':
                    data = await DeclarationFetchHelper(formDb, user_id)
                    return {"status_code": 200, "success": True, "data": data}

        else:
            return HTTPException(status_code=401)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


