
class CreateDatabaseTables:
    def __init__(self, initDb):
        self.initDb = initDb
        
    async def create_table_users(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    "first_name" text,
                    "last_name" text,
                    "phone" text,
                    "email" text,
                    "user_id" integer,
                    "session" text
                )
                """
            )
            
    async def create_table_login_otp(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS login_otp(
                    "email" text,
                    "otp" integer
                )
                """
            )
            
    async def create_table_saved_jobs(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS saved_jobs(
                    "user_id" integer,
                    "email" text,
                    "job_id" text,
                    "job_name" text,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
         
    async def create_table_jobs_applied(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs_applied(
                    "user_id" integer,
                    "email" text,
                    "job_id" integer,
                    "job_title" text,
                    "application_status" text,
                    "rejected" boolean,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_personal_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS personal_data(
                    "user_id" integer,
                    "first_name" text,
                    "last_name" text,
                    "phone" text,
                    "email" text,
                    "dob" text,
                    "nationality" text,
                    "current_address" text,
                    "current_state" text,
                    "current_city" text,
                    "current_pincode" text,
                    "permanent_address" text,
                    "permanent_state" text,
                    "permanent_city" text,
                    "permanent_pincode" text,
                    "hire_you_desc" text,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_files_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS files_data(
                    "user_id" integer,
                    "which_file" text,
                    "file_type" text,
                    "file_id" integer,
                    "file_name" text,
                    "file_size" integer,
                    "file_base64" text,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_education_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS education_data(
                    "user_id" integer,
                    "degree" text,
                    "major" text,
                    "institution" text,
                    "start_date" text,
                    "end_date" text,
                    "grade" text,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_certification_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS certification_data(
                    "user_id" integer,
                    "name" text,
                    "desc" text,
                    "file" boolean,
                    "file_id" integer,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_achievements_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS achievements_data(
                    "user_id" integer,
                    "name" text,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_experience_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS experience_data(
                    "user_id" integer,
                    "fresher" boolean,
                    "employeer" text,
                    "job_role" text,
                    "start_date" text,
                    "end_date" text,
                    "exp" integer,
                    "current_ctc" integer,
                    "expected_ctc" integer,
                    "desc" text,
                    "skills" Text[],
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    async def create_table_declaration_data(self):
        async with self.initDb.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS declaration_data(
                    "user_id" integer,
                    "applied_job_id" integer,
                    "applied_job_name" text,
                    "gender" text,
                    "declaration_accepted" boolean,
                    "physical_disability" Text[],
                    "medical_issue" Text[],
                    "criminal_record" text,
                    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    "modifiedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
    
            