from datetime import datetime
from db.prisma import db
from flask import jsonify

async def insert_job(job):
    await db.connect()

    try:
        def to_lowercase(value):
            return value.lower() if isinstance(value, str) else 'n/a'
        
        company_name = job.get('company_name')
        if not company_name:
            return jsonify({"error": "Company Name is required"})
        
        # Await the asynchronous call to find the company
        company = await db.company.find_unique(where={'company_name': company_name})
        if not company:
            company_document = {
                "company_name": to_lowercase(job.get('company_name', 'N/A')),
                "company_logo": job.get('company_logo'),
                "description": job.get('company_desc')
            }
            # Await the asynchronous call to create the company
            company = await db.company.create(data=company_document)
            print(company, "here is company ======>")
            
        # Convert all fields to lowercase
        job_document = {
            "title": to_lowercase(job.get('title', 'N/A')),
            "job_link": job.get('job_link', 'N/A'),
            "job_location": to_lowercase(job.get('job_location', 'N/A')),
            "job_type": to_lowercase(job.get('job_type', 'N/A')),
            "job_salary": job.get('job_salary', None),
            "source": to_lowercase(job.get('source', 'N/A')),
            "posted": job.get('posted', datetime.utcnow()),
            "companyId": company.id  # Access the id of the company object
        }

        # Validate input

        # Await the asynchronous call to create the job
        job = await db.job.create(data=job_document)
        print("job created")
        return job 
    
    except Exception as e:
        print(e, "Error from insert_job function")  # Output the error to the console for debugging
        return {'error': str(e)}, 500
    
    finally:
        await db.disconnect()
