from fastapi import APIRouter, Request
import asyncpg
import traceback

router = APIRouter()

@router.post("/delete_jobs")
async def delete_jobs(request: Request):
    data = await request.json()
    try:
        pool = await asyncpg.create_pool(
        user="postgres", database="career", host="localhost"
        )
        async with pool.acquire() as connection:
            
            await connection.execute(
                """
                DELETE FROM jobs WHERE job_title = $1
                """,
                data['job_title']
            )
        return{f"job DELETED : {data['job_title']}" }
    
    except Exception as e:
        print(e)
        traceback.print_exc()








# from fastapi import APIRouter, Request
# from sqlalchemy.orm import Session
# from. import models, database

# router = APIRouter()

# @router.post("/delete_jobs")
# async def delete_jobs(request: Request):
#     data = await request.json()
#     db = Session(database.engine)
#     try:
#         job = db.query(models.Job).filter_by(job_title=data['job_title']).first()
#         if job:
#             db.delete(job)
#             db.commit()
#             return {"message": f"Job deleted: {data['job_title']}"}
#         else:
#             return {"error": "Job not found."}
#     finally:
#         db.close()