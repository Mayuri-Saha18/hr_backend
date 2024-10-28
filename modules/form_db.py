import asyncpg
import logging
import traceback
import json, sys
from datetime import datetime
from modules.authentication_db import AuthenticationDB


class FormDB:
    def __init__(self, initDb):
        self.initDb = initDb
        
    
    # all save functions

    async def save_data_personal(self, user_id, fname, lname, phone, email, dob, nationality, current_address, current_state, current_city, current_pincode, permanent_address, permanent_state, permanent_city, permanent_pincode, hire_you_desc, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT INTO personal_data (user_id, first_name, last_name, phone, email, dob, nationality, current_address, current_state, current_city, current_pincode, permanent_address, permanent_state, permanent_city, permanent_pincode, hire_you_desc, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
                """,
                user_id, fname, lname, phone, email, dob, nationality, current_address, current_state, current_city, current_pincode, permanent_address, permanent_state, permanent_city, permanent_pincode, hire_you_desc, created, modified
            )
            return {"success": True}
        
    
    async def save_files_data(self, user_id, which_file, file_type, file_id, file_name, file_size, file_base64, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into files_data(user_id, which_file, file_type, file_id, file_name, file_size, file_base64, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                user_id, which_file, file_type, file_id, file_name, file_size, file_base64, created, modified
            )
        
    
    async def save_data_education(self, user_id, degree, major, institution, start_date, end_date, grade, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into education_data(user_id, degree, major, institution, start_date, end_date, grade, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                user_id, degree, major, institution, start_date, end_date, grade, created, modified
            )
            

     
    async def save_data_certification(self, user_id, name, desc, file, file_id, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into certification_data(user_id, name, desc, file, file_id, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                user_id, name, desc, file, file_id, created, modified
            )
            
            
    async def save_data_achievements(self, user_id, name, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into achievement_data(user_id, which_file, file_type, file_id, file_name, file_size, file_base64, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                user_id, name, created, modified
            )
            
            
    async def save_data_experience(self, user_id, fresher, employeer, job_role, start_date, end_date, exp, current_ctc, expected_ctc, desc, skills, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into experience_data(user_id, fresher, employeer, job_role, start_date, end_date, exp, current_ctc, expected_ctc, "desc", skills, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
                user_id, fresher, employeer, job_role, start_date, end_date, exp, current_ctc, expected_ctc, desc, skills, created, modified
            )
            

    async def save_data_declaration(self, user_id, applied_job_id, applied_job_name, gender, declaration_accepted, physical_disability, medical_issue, criminal_record, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into declaration_data(user_id, applied_job_id, applied_job_name, gender, declaration_accepted, physical_disability, medical_issue, criminal_record, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """,
                user_id, applied_job_id, applied_job_name, gender, declaration_accepted, physical_disability, medical_issue, criminal_record, created, modified
            )
 
            
    async def save_data_jobs_applied(self, user_id, email, applied_job_id, applied_job_name, application_status, rejected, created, modified):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                    INSERT into jobs_applied(user_id, email, job_id, job_title, application_status, rejected, "createdAt", "modifiedAt")
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                user_id, email, applied_job_id, applied_job_name, application_status, rejected, created, modified
            )
    
    
    # All fetch functions

    async def fetch_data_personal(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetchrow(
                """
                    SELECT * from personal_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
        
    async def fetch_files_data(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                    SELECT * from files_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
            
    async def fetch_data_education(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                    SELECT * from education_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
            
    async def fetch_data_certification(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                    SELECT * from certification_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
            
    async def fetch_data_achievements(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                    SELECT * from achievements_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
    
    async def fetch_data_experience(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                    SELECT * from experience_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
    
    async def fetch_data_declaration(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                    SELECT * from declaration_data WHERE user_id = $1
                """,
                user_id
            )
            return {"success": True, "data": data}
            
           
    