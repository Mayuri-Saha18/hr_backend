postgres + pgadmin :
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads


Make a config.json file.

<!-- config.json -->
```json
{   
    "db_host": "localhost",
    "db_user": "postgres",
    "db_password": "Your_Password",
    "db_name": "Your_Database_Name",

    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "hr_email": "Your_Email",
    "hr_password": "Your_SMTP_Password",
    "default_email_subject": "Email_Subject",
}
```