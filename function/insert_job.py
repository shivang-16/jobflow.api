from datetime import datetime
from db.prisma import db

async def insert_job(job):
    await db.connect()

  
    print("inside job", job)
    def to_lowercase(value):
        return value.lower() if isinstance(value, str) else 'n/a'

    # Convert all fields to lowercase
    job_document = {
        "title": to_lowercase(job.get('title', 'N/A')),
        "company_name": to_lowercase(job.get('company_name', 'N/A')),
        "job_link": to_lowercase(job.get('job_link', 'N/A')),
        "job_location": to_lowercase(job.get('job_location', 'N/A')),
        "job_salary": job.get('job_salary', 'N/A'),
        "source": to_lowercase(job.get('source', 'N/A')),
        "posted": job.get('posted', datetime.utcnow()),
    }
    print(dir(db), "here is")

    # Validate input
    try:
        # Assuming 'db.job.create' is correctly set as async
        job = await db.job.create(data=job_document)
        print("job created")
        return job  # Return the created job object
    
    except Exception as e:
        print(e, "from insert")  # Output the error to the console for debugging
        # Return a dictionary instead of 'jsonify' in an async context
        return {'error': str(e)}, 500
    
    finally:
        await db.disconnect()
