from flask import Blueprint, request, jsonify
from function.crawler.crawler import scrapejobsdata
from db.prisma import db

job_blueprint = Blueprint('job', __name__)

@job_blueprint.route('/', methods=['GET'])
async def create_job():   
    try:
        await scrapejobsdata()
        return "Successfully inserted job", 201
    
    except Exception as e:
        print(e, "Error in create_job function")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    

def serialize_job(job):
    return {
        'id': job.id,
        'title': job.title,
        'company_name': job.company_name,
        'job_location': job.job_location,
        'job_salary': job.job_salary,
        'job_link': job.job_link,
        'source': job.source
    }

@job_blueprint.route('/get', methods=['GET'])
async def get_job():   
    try:
        await db.connect()

        page = request.args.get('page', default=1, type=int)
        source = request.args.get('portal', default=None, type=str)
        title = request.args.get('title', default=None, type=str)

        if page < 1:
            return jsonify({'error': "Page must be a positive number"}), 400
        
        page_size = 10
        skip = (page - 1) * page_size

        filter = {}
        if source: 
            filter['source'] = source
        if title:
            filter['title'] = {"contains": title}

        # Fetch jobs from the database
        jobs = await db.job.find_many(
            where=filter,
            skip=skip,
            take=page_size
        )

        # Serialize the job data
        serialized_jobs = [serialize_job(job) for job in jobs]

        return jsonify({'jobs': serialized_jobs, 'page': page, 'page_size': page_size}), 200

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Disconnect Prisma client
        await db.disconnect()

