from db.prisma import db
from flask import g

async def checkExistingJob(jobdata):
    try:
        await db.connect()

        title = jobdata['title'].lower()
        print(title, g.user.id, "here is the user id")

        # Find tracked job for this user where the related job has matching title
        existing_job = await db.tracked_jobs.find_first(
            where={
                'userId': g.user.id,
                'job': {
                    'title': title
                }
            },
            include={
                'job': {
                    'include': {
                        'company': True
                    }
                }
            }
        )

        # If job doesn't exist, return None
        if not existing_job:
            return jobdata

        print(existing_job, "here is the existing job")
        
        # Get company details safely
        company = existing_job.job.company if existing_job.job else None
        
        formatted_job = {
            "userId": g.user.id,
            "title": existing_job.job.title.upper(),
            "status": existing_job.status,
            "company_name": company.company_name if company else None,
            "company_logo": company.company_logo if company else None,
            "job_link": existing_job.job.job_link,
            "job_type": existing_job.job.job_type,
            "job_location": existing_job.job.job_location,
            "job_salary": existing_job.job.job_salary,
            "source": existing_job.job.source
        }
        
        return formatted_job
            
            
    except Exception as e:
        print(e, "Error in checkExistingJob function")
        return jobdata
    finally:
        await db.disconnect()