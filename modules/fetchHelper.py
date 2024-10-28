async def PersonalFetchHelper(db, user_id):
    try:
        files_data = await db.fetch_files_data(int(user_id))
        personal_data = await db.fetch_data_personal(int(user_id))
        photo = [
            {
                "id": file['file_id'],
                "name": file['file_name'],
                "type": file['file_type'],
                "size": file['file_size'],
                "base64": file['file_base64'],
                
            }
            for file in files_data['data']
            if file['which_file'] == 'photo'
        ]
        resumes = [
            {
                "id": file['file_id'],
                "name": file['file_name'],
                "type": file['file_type'],
                "size": file['file_size'],
                "base64": file['file_base64'],
                
            }
            for file in files_data['data']
            if file['which_file'] == 'resume'
        ]
        data = dict(personal_data['data'].items())
        data['resumes'] = resumes
        data['photo'] = photo
        return data
    
    except Exception as e:
        print(e)
        
        
async def EducationFetchHelper(db, user_id):
    try:
        education_data = await db.fetch_data_education(int(user_id))
        certification_data = await db.fetch_data_certification(int(user_id))
        achievements_data = await db.fetch_data_achievements(int(user_id))
        data_e = []
        data_c = []
        data_a = []
        
        if len(education_data['data'])  > 0:
            for i,e in enumerate(education_data['data']):
                data_e = [dict(education_data['data'][i].items())]
        
        if len(certification_data['data'])  > 0:
            for i,c in enumerate(certification_data['data']):
                data_c = [dict(certification_data['data'][i].items())]
            
        if len(achievements_data['data'])  > 0:
            for i,a in enumerate(achievements_data['data']):
                data_a = [dict(achievements_data['data'][i].items())]
            
        data = {
            "education": data_e,
            "certifications": data_c,
            "achievements": data_a
        }
        return data
    
    except Exception as e:
        print(e)
        
        
async def ProfessionalFetchHelper(db, user_id):
    try:
        experience_data = await db.fetch_data_experience(int(user_id))
        data_e = []
        global fresher
        
        if len(experience_data['data'])  > 0:
            for i,e in enumerate(experience_data['data']):
                fresher = experience_data['data'][i]['fresher']
                data_e = [dict(experience_data['data'][i].items())]
        data = {
            "fresher": fresher,
            "data": data_e
        }
        return data
    
    except Exception as e:
        print(e)
        
        
async def DeclarationFetchHelper(db, user_id):
    try:
        declaration_data = await db.fetch_data_declaration(int(user_id))
        if len(declaration_data['data']) > 0:
            data = dict(declaration_data['data'][0].items())
            return data
    
    except Exception as e:
        print(e)