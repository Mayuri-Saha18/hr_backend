from fastapi import FastAPI, Depends, Request, HTTPException
# from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, sys, json
# from admin.admin import router as admin_router
from eps.auth_route import auth_router
from eps.form_route import form_router
from eps.static_route import static_router
# from eps.send_file import router as file_router
# from eps.verify_otp import router as verify_router
# from eps.user_data import router as user_router
# from eps.profile import router as profile_router
# from eps.jobs import router as jobs_router
# from eps.applications import router as application_router
sys.path.append("/home/ubuntu/GOURAB_UBUNTU/HR_Portal/server_hr/modules")
from modules.email import EmailService
from dependencies import get_db_init_obj, create_all_tables , initializeAuthDb

app = FastAPI()

async def startup_event():
    await get_db_init_obj()
    await create_all_tables()
    await initializeAuthDb()
    print("Database Success")
app.add_event_handler("startup", startup_event)


origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000'] 

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin', "Set-Cookie"],
)

# app.add_middleware(
#     SessionMiddleware,
#     secret_key="1234",
# )

app.include_router(auth_router, tags=["otp"])
app.include_router(static_router, tags=["static"])
app.include_router(form_router, prefix='/applicationform')

@app.get("/getJobs")
async def get_jobs():
    with open("jobs.json", "r") as f:
        data = json.load(f)
        return {"success": True, "data": data}


@app.get("/getJob")
async def get_jobs_by_id(id: int):
    with open("jobs.json", "r") as f:
        data = json.load(f)
        for job in data:
            if id == job["job_id"]:
                return {"success": True, "data": job}

# app.include_router(verify_router, tags=["verify"])
# app.include_router(profile_router, tags=["profile"])
# app.include_router(file_router, tags=["file"])
# # app.include_router(application_router, tags=["application"])
# app.include_router(user_router, tags=["user_data"])
# app.include_router(jobs_router, tags=["jobs"])
# app.include_router(admin_router, prefix="/admin", tags=["users"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
    
    
