# from fastapi import APIRouter, HTTPException, Depends, Request
# from modules.authentication_db import AuthenticationDB
# from modules.email import EmailService
# import random
# from dependencies import initializeAuthDb
# router = APIRouter()

# # authDb = AuthenticationDB()
# # @router.on_event("startup")
# # @router.on_event("startup")
# # async def on_startup():
# #     # global init_db
# #     # global auth_db
# #     init_db = InitDB()
# #     await init_db.initialize()
# #     global auth_db
# #     auth_db = AuthenticationDB(init_db)


# # def get_auth_db(auth_db: AuthenticationDB = Depends()):
# #     print(auth_db)

# class EmailData(BaseModel):
#     email: str

# email_service = EmailService()


# def generate_otp():
#     otp = random.randint(100000, 999999)
#     # exp = datetime.now() + timedelta(minutes=5)
#     # exp_unix = int(exp.timestamp())
#     # otp = f"{rnd}_{exp_unix}"
#     return otp


# # @router.post("/send_otp")
# # @router.post("/login")

# # def call_send_otp(authDb):
# #     return authDb
# @router.post("/login")
# async def send_otp(request: Request, auth_db: AuthenticationDB = Depends(initializeAuthDb)):
#     otp = str(generate_otp())
#     print(auth_db.initDb.pool)
#     print(otp)
#     # try:
#     #     email_service.send_otp(email_data.email, otp)
#     #     await auth_db.delete_otp(email_data.email)
#     #     await auth_db.insert_otp(email_data.email, otp)
#     #     return {"success": True, "message": "OTP sent to your email."}
#     # except Exception as e:
#     #     raise HTTPException(status_code=500, detail=str(e))
    

