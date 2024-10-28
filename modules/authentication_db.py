import sys
from datetime import datetime
from modules.initializeDb import InitDB 

class AuthenticationDB:
    def __init__(self, initDb):
        self.initDb = initDb
    
            
    async def delete_otp(self, email):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                DELETE FROM login_otp WHERE email = $1
                """,
                email,
            )
            

    async def check_otp(self, email):
        timee = str(datetime.now().timestamp())
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            otp_expiry = await connection.fetchval(
                """
                SELECT otp FROM login_otp WHERE email = $1
                """,
                email,
            )
            return False
            # exp = otp_expiry.split("_")[1]
            
            # if exp > timee :
            #     return False
            # else:
            #     return True
            
            
    async def user_data_from_db(self):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            result = await connection.fetch(
                """
                SELECT * FROM users
                """
                )
            return result
        
        
    # async def edit_user_data(self, email, name=None, phone=None, address=None):
    #     if not self.initDb.pool:
    #         raise Exception("Database pool is not initialized")

    #     # Prepare the SQL statement dynamically based on the fields provided
    #     set_clauses = []
    #     params = []  # Initialize an empty list for parameters

    #     if name:
    #         set_clauses.append(f"name = ${len(params) + 1}")
    #         params.append(name)
    #     if phone:
    #         set_clauses.append(f"phone = ${len(params) + 1}")
    #         params.append(phone)
    #     if address:
    #         set_clauses.append(f"address = ${len(params) + 1}")
    #         params.append(address)

    #     if not set_clauses:
    #         raise ValueError("At least one field to update must be provided")

    #     params.append(email)

    #     set_clause_str = ", ".join(set_clauses)
    #     sql = f"""
    #     UPDATE users SET {set_clause_str} WHERE email = ${len(params)}
    #     """ 

    #     logging.info(f"Executing SQL: {sql}")
    #     logging.info(f"With params: {params}")

    #     async with self.initDb.pool.acquire() as connection:
    #         result = await connection.execute(sql, *params)
    #         if result == "UPDATE 0":
    #             raise asyncpg.exceptions.NoDataFoundError("User not found.")
    #     return result


    async def insert_otp(self, email, otp):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            emails = await connection.fetchval(
                """
                SELECT email FROM login_otp WHERE email = $1
                """,
                email
            )

            if emails == email:
                await connection.execute(
                    """
                    UPDATE login_otp SET otp = $1 WHERE email = $2
                    """,
                    otp, email
                )
            else:
                await connection.execute(
                    """
                    INSERT INTO login_otp (email, otp)
                    VALUES ($1, $2)
                    """,
                    email, otp
                )


    async def save_user(self, fname, lname, phone, email):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
                await connection.execute(
                    """
                    UPDATE users SET first_name = $1, last_name = $2, phone = $3 WHERE email = $4
                    """,
                    fname, lname, phone, email
                )   
                return {"success": True, "message":"Userdata Saved"}
        
    
    async def check_user(self, email):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            existing_record = await connection.fetch(
                """
                SELECT * FROM users WHERE email = $1
                """,
                email
            )
            return {"success": True, "data": existing_record}


    async def get_otp(self, email):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            result = await connection.fetchval(
                """
                SELECT otp FROM login_otp WHERE email = $1
                """,
                email,
            )
            return result
        
    
    async def remove_otp_record(self, email):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                DELETE FROM login_otp WHERE email = $1
                """,
                email,
            )
            return {"success": True}


    async def insert_session(self, email, session, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
       
        async with self.initDb.pool.acquire() as connection:
 
            emails = await connection.fetchval(
                """
                SELECT email FROM users WHERE email = $1
                """,
                email
            )
            if email == emails:
                await connection.execute(
                    """
                    UPDATE users SET session = $1, user_id = $3 WHERE email = $2
                    """,
                    session, email, user_id
                )
            else:
                await connection.execute(
                    """
                    INSERT INTO users (session, email, user_id)
                    VALUES ($1, $2, $3)
                    """,
                    session, email, user_id
                )


    async def delete_session(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
       
        async with self.initDb.pool.acquire() as connection:
            user = await connection.execute(
                    """
                    SELECT FROM users WHERE user_id = $1
                    """,
                    user_id
                )
            if not user:
                return {"success": "error", "message": "User not found."}
            
            await connection.execute(
                """
                UPDATE users SET session = NULL WHERE user_id = $1
                """,
                user_id,
            )


    async def add_otp(self, otp):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            otp = await connection.fetchrow(
                """
                SELECT otp FROM login_otp
                """
            )

            await connection.fetchrow(
                """
                UPDATE users SET otp = $1
                """,
                otp
            )


    async def get_id(self, email):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            user_id = await connection.fetchrow(
                """
                SELECT user_id FROM users WHERE email = $1
                """,
                email
            )
        return user_id
    
    
    async def get_user(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            user = await connection.fetchrow(
                """
                SELECT * FROM users WHERE user_id = $1
                """,
                user_id
            )
            return user
        
        
    
    async def get_jobs_applied(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                SELECT * FROM jobs_applied WHERE user_id = $1
                """,
                user_id
            )
            return data
        
    
    async def get_saved_jobs(self, user_id):
        if not self.initDb.pool:
            raise Exception("Database pool is not initialized")
        async with self.initDb.pool.acquire() as connection:
            data = await connection.fetch(
                """
                SELECT * FROM saved_jobs WHERE user_id = $1
                """,
                user_id
            )
            return data
        
    # Check if a job is already saved for the user
    async def is_job_saved(self, user_id, job_id):
        async with self.initDb.pool.acquire() as connection:
            saved_job = await connection.fetchrow(
                "SELECT 1 FROM saved_jobs WHERE user_id = $1 AND job_id = $2",
                user_id, job_id
            )
            return saved_job is not None

    # Method to save a job for a user
    async def save_job(self, user_id, job_id):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                "INSERT INTO saved_jobs (user_id, job_id) VALUES ($1, $2)", user_id, job_id
            )

    # Method to remove (un-save) a job for a user
    async def remove_saved_job(self, user_id, job_id):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                "DELETE FROM saved_jobs WHERE user_id = $1 AND job_id = $2", user_id, job_id
            )