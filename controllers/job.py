from flask import Blueprint, request, jsonify
from function.crawler.crawler import scrapejobsdata
from db.prisma import db
from utils import serialize_job

job_blueprint = Blueprint('job', __name__)

@job_blueprint.route('/', methods=['GET'])
async def create_job():   
    try:
        await scrapejobsdata()
        return "Successfully inserted job", 201
    
    except Exception as e:
        print(e, "Error in create_job function")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    



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

        # Fetch jobs from the database including the company relation
        jobs = await db.job.find_many(
            where=filter,
            skip=skip,
            take=page_size,
            include={'company': True}  # Include the company relation
        )

        # Serialize the job data
        serialized_jobs = [job.model_dump() for job in jobs]

        return jsonify({'jobs': serialized_jobs, 'page': page, 'page_size': page_size}), 200

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Disconnect Prisma client
        await db.disconnect()


@job_blueprint.route('/get/id', methods=['GET'])
async def getJobId():   
    try:
        await db.connect()

        jobId = request.args.get('jobId', default=1, type=int)

        # Fetch jobs from the database including the company relation
        job = await db.job.find_unique(
            where={"id": jobId},
        )

        # Serialize the job data
        serialized_job = serialize_job(job) 

        return jsonify({'job': serialized_job }), 200

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Disconnect Prisma client
        await db.disconnect()

@job_blueprint.route('/get/company/list', methods=['GET'])
async def get_companies_list():   
    try:
        await db.connect()

        # Fetch jobs from the database including the company relation
        companies = await db.company.find_many()

        serialized_companies = [company.model_dump() for company in companies]
        return jsonify({'companies': serialized_companies}), 200

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Disconnect Prisma client
        await db.disconnect()
