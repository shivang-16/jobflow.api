from db.prisma import db
from flask import jsonify, request, Blueprint, g

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/get', methods=['GET'])
async def get_user():
    await db.connect()
    try:
    
        currentUser = g.user

        user = await db.user.find_unique(where={"id": currentUser.id})
        if not user:
            return jsonify({"error": "User not exists"}), 400
        
        user_dict = user.model_dump() 
        
        print(user_dict, "Fetched User")
        return jsonify({"success": True, "user": user_dict}), 200
    
    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Disconnect Prisma client
        await db.disconnect()

@user_blueprint.route('/job/apply', methods=['POST'])
async def apply_job():
    # Find the job by its ID
    jobId = request.args.get('jobId', default=None, type=str)
    if not jobId:
        return jsonify({"error": "JobId is missing"}), 400

    job = await db.job.find_unique(where={"id": jobId})
    if not job:
        return jsonify({"error": "Job not exists"}), 404
    
    # Get the current user from the request context
    currentUser = g.user
    applied_job = await db.applied_jobs.find_unique(where={"userId": currentUser.id, "jobId": jobId})
    if applied_job:
        return jsonify({"error": "Job already applied"}), 400
    
    # Update the user to connect the job
    await db.applied_jobs.create(
        data={
            "userId": currentUser.id,
            "jobId": jobId
        }
    )
    
    return jsonify({"success": True, "message": "Job saved to user"}), 200

@user_blueprint.route('/job/update/status', methods=['POST'])
async def update_job_status():

    jobId = request.args.get('jobId', default=None, type=str)
    status = request.args.get('status', default=None, type=str)

    if not jobId or not status:
        return jsonify({"error": "JobId or Status is"}), 400

    # Find the job by its ID
    job = await db.job.find_unique(where={"id": jobId})
    if not job:
        return jsonify({"error": "Job not exists"}), 404
    
    # Get the current user from the request context
    currentUser = g.user
    applied_job = await db.applied_jobs.find_unique(where={"userId": currentUser.id, "jobId": jobId})
    if applied_job:
        return jsonify({"error": "Job already applied"}), 400
    
    # Update the user to connect the job
    await applied_job.update(
        data={
            "status": status
        }
    )
    
    return jsonify({"success": True, "message": "Job saved to user"}), 200


@user_blueprint.route('/job/bookmark', methods=['POST'])
async def bookmark_job():

    jobId = request.args.get('jobId', default=None, type=str)
    if not job:
        return jsonify({"error": "Job not exists"}), 400

    # Find the job by its ID
    job = await db.job.find_unique(where={"id": jobId})
    if not job:
        return jsonify({"error": "Job not exists"}), 404
    
    # Get the current user from the request context
    currentUser = g.user
    user = await db.user.find_unique(where={"id": currentUser.id})
    if not user:
        return jsonify({"success": False, "message": "User not exists"}), 400
    
    await db.user.update(
        where={"id": currentUser.id},
        data={
            "bookmarked_jobs": {
                "push": jobId  # Use 'push' to add the jobId to the array
            }
        }
    )
    
    return jsonify({"success": "Job saved to user"}), 200
