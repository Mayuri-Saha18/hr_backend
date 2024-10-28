async def PersonalSubmitHelper(data, db, created, modified):
    try:
        await db.save_data_personal(
            data["user_id"],
            data["fname"],
            data["lname"],
            data["phone"],
            data["email"],
            data["dob"],
            data["nationality"],
            data["current_address"],
            data["current_state"],
            data["current_city"],
            data["current_pincode"],
            data["permanent_address"],
            data["permanent_state"],
            data["permanent_city"],
            data["permanent_pincode"],
            data["hire_you_desc"],
            created,
            modified,
        )

        for resume in data["resumes"]:
            which_file = "resume"
            await db.save_files_data(
                data["user_id"],
                which_file,
                resume["type"],
                resume["id"],
                resume["name"],
                resume["size"],
                resume["base64"],
                created,
                modified,
            )

        for photo in data["photo"]:
            which_file = "photo"
            await db.save_files_data(
                data["user_id"],
                which_file,
                photo["type"],
                photo["size"],
                photo["name"],
                photo["size"],
                photo["base64"],
                created,
                modified,
            )
    except Exception as e:
        print(e)


async def EducationSubmitHelper(data, db, created, modified):
    try:
        if len(data["education"]) > 0:
            for each in data["education"]:
                await db.save_data_education(
                    data["user_id"],
                    each["degree"],
                    each["major"],
                    each["institution"],
                    each["start_date"],
                    each["end_date"],
                    each["grade"],
                    created,
                    modified,
                )

        if len(data["certifications"]) > 0:
            for each in data["certifications"]:
                await db.save_data_certification(
                    data["user_id"],
                    each["name"],
                    each["desc"],
                    each["file"],
                    each["file_id"],
                    created,
                    modified,
                )

        if len(data["achievements"]) > 0:
            for each in data["achievements"]:
                await db.save_data_achievements(
                    data["user_id"], each["name"], created, modified
                )
    except Exception as e:
        print(e)


async def ProfessionalSubmitHelper(data, db, created, modified):
    try:
        if len(data["data"]) > 0:
            for each in data["data"]:
                await db.save_data_experience(
                    data["user_id"],
                    False,
                    each["employeer"],
                    each["job_role"],
                    each["start_date"],
                    each["end_date"],
                    int(each["exp"]),
                    int(each["current_ctc"]),
                    int(each["expected_ctc"]),
                    str(each["desc"]),
                    each["skills"],
                    created,
                    modified,
                )
    except Exception as e:
        print(e)


async def DeclarationSubmitHelper(data, db, created, modified):
    try:
        physical_disability = []
        medical_issue = []
        physical_disability.append(data["has_physical_disability"])
        physical_disability.append(data["what_physical_disability"])
        medical_issue.append(data["has_medical_issue"])
        medical_issue.append(data["what_medical_issue"])
        await db.save_data_declaration(
            data["user_id"],
            data["applied_job_id"],
            data["applied_job_name"],
            data["gender"],
            data['declaration_accepted'],
            physical_disability,
            medical_issue,
            data["has_criminal_record"],
            created,
            modified,
        )
    except Exception as e:
        print(e)


async def JobsAppliedSubmitHelper(data, email, db, created, modified):
    try:
        await db.save_data_jobs_applied(
            data["user_id"],
            email,
            data["applied_job_id"],
            data["applied_job_name"],
            "Pending",
            False,
            created,
            modified,
        )
    except Exception as e:
        print(e)
