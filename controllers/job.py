from flask import Blueprint, request, jsonify
from function.crawler import scrapejobsdata
from function.insert_job import insert_job
from db.prisma import db

job_blueprint = Blueprint('job', __name__)

@job_blueprint.route('/', methods=['GET'])
async def create_job():   
    try:
        job = {
        "title": 'Developer (Entry Level)',
        "company_name": "Planned Systems International",
        "job_link": "https://www.linkedin.com/jobs/view/jr-web-developer-entry-level-at-planned-systems-international-3940392184?position=2&pageNum=0&refId=%2BAujncr6Zsx2KvlKN5TXyg%3D%3D&trackingId=ysJFVkM0rnaN6sc4gX9PkQ%3D%3D",
        "job_location": "United States",
        "source": "linkedin",
        }

        job = await insert_job(job)
        return dict(job), 201
    
    except Exception as e:
        print(e, "here is the erorr")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500

