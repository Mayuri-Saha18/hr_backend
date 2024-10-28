from modules.initializeDb import InitDB
from modules.authentication_db import AuthenticationDB
from modules.createTable import CreateDatabaseTables
from modules.form_db import FormDB

init_db = InitDB()

async def get_db_init_obj() -> InitDB:
    await init_db.initialize()
    return init_db


async def initializeAuthDb():
    if init_db.pool is not None:
        auth_db = AuthenticationDB(init_db)
        return auth_db
    
async def initializeFormDb():
    if init_db.pool is not None:
        form_db = FormDB(init_db)
        return form_db
    

async def create_all_tables():
    if init_db.pool is not None:
        tables_created = CreateDatabaseTables(init_db)
        if tables_created:
            # users, authentication
            await tables_created.create_table_users()
            await tables_created.create_table_login_otp()
            await tables_created.create_table_jobs_applied()
            await tables_created.create_table_saved_jobs()
            
            # application
            await tables_created.create_table_personal_data()
            await tables_created.create_table_files_data()
            await tables_created.create_table_education_data()
            await tables_created.create_table_certification_data()
            await tables_created.create_table_achievements_data()
            await tables_created.create_table_experience_data()
            await tables_created.create_table_declaration_data()
            
            # admin
            
            print("Tables Created")