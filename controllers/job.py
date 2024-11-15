from flask import Blueprint, request, jsonify
from function.crawler.crawler import scrapejobsdata

job_blueprint = Blueprint('job', __name__)

@job_blueprint.route('/', methods=['GET'])
async def create_job():   
    try:
        await scrapejobsdata()
        return "Successfully inserted job", 201
    
    except Exception as e:
        print(e, "here is the erorr")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500

