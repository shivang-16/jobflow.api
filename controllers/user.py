from db.prisma import db
from flask import jsonify, request, Blueprint, g
from utils import serialize_job
from function.insert_job import insert_job
from datetime import datetime

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/get', methods=['GET'])
async def get_user():
   
    try:
        await db.connect()
    
        currentUser = g.user

        user = await db.user.find_unique(where={"id": currentUser.id})
        if not user:
            return jsonify({"error": "User not exists"}), 400
        
        user_dict = user.model_dump() 
        
        return jsonify({"success": True, "user": user_dict}), 200
    
    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Disconnect Prisma client
        await db.disconnect()


@user_blueprint.route('/update', methods=['PUT'])
async def update_user():
    try:
        # Connect to the database
        await db.connect()

        currentUser = g.user

        # Fetch the current user from the database
        user = await db.user.find_unique(where={"id": currentUser.id})
        if not user:
            return jsonify({"error": "User does not exist"}), 400

        # Get the request data
        body_data = request.get_json()

        print(body_data, "here is body dat")

        # Prepare the fields to update
        update_data = {}

        # Update name if provided
        if 'name' in body_data and body_data['name']:
            update_data['name'] = body_data['name']

        # Update email if provided
        if 'email' in body_data and body_data['email']:
            update_data['email'] = body_data['email']

        # Update job_statuses if provided
        if 'job_statuses' in body_data and isinstance(body_data['job_statuses'], list):
            update_data['job_statuses'] = [status.lower() for status in body_data['job_statuses']]


        print(update_data, "here is updatedata")
        # If there are fields to update, perform the update
        if update_data:
            updated_user = await db.user.update(
                where={"id": currentUser.id},
                data=update_data
            )

            user_dict = updated_user.model_dump() 
            return jsonify({"success": True, "user": user_dict}), 200
        else:
            return jsonify({"error": "No valid fields to update"}), 400

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500

    finally:
        # Disconnect Prisma client
        await db.disconnect()

@user_blueprint.route('/jobs/get', methods=['GET'])
async def get_user_jobs():
    try:
        await db.connect()

        # Get user ID from the request context
        userId = g.user.id
        user = await db.user.find_unique(where={"id": userId})
        if not user:
            return jsonify({"success": False, "error": "User not exists"}), 404

        # Get status from query parameters
        status = request.args.get('status', default='', type=str)
        print(f"Filtering jobs with status: {status}")

        # Fetch user's applied jobs
        userAppliedJobs = await db.tracked_jobs.find_many(
            where={"userId": user.id},
            include={
                'job': {
                    'include': {'company': True}
                }
            }
        )
        jobs_serialized = [job.model_dump() for job in userAppliedJobs]
        return jsonify({"success": True, "jobs": jobs_serialized}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        print("Disconnecting from the database...")
        await db.disconnect()
        print("Disconnected from the database.")



@user_blueprint.route('/job/apply', methods=['POST'])
async def apply_job():
    try:
        await db.connect()

        # Find the job by its ID
        jobId = request.args.get('jobId', default=None, type=str)
        if not jobId:
            return jsonify({"success": False, "error": "JobId is missing"}), 400

        job = await db.job.find_unique(where={"id": jobId})
        if not job:
            return jsonify({"success": False, "error": "Job does not exist"}), 404

        # Get the current user from the request context
        currentUser = g.user

        # Check if the job has already been applied for by the user
        applied_job = await db.tracked_jobs.find_first(
            where={"userId": currentUser.id, "jobId": jobId}
        )
        if applied_job:
            return jsonify({"success": False, "error": "Job already applied"}), 400

        # Create the application entry
        await db.tracked_jobs.create(
            data={
                "userId": currentUser.id,
                "jobId": jobId,
                "status": 'applied'
            }
        )

        return jsonify({"success": True, "message": "Job added to tracker"}), 200

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        await db.disconnect()



@user_blueprint.route('/job/update/status', methods=['PUT'])
async def update_job_status():

    try:
        await db.connect()
        jobId = request.args.get('jobId', default=None, type=str)
        status = request.args.get('status', default=None, type=str)

        print(jobId, status, "here are jobid and status")

        if not jobId or not status:
            return jsonify({"success": False, "error": "JobId or Status is"}), 400

        
        # Get the current user from the request context
        currentUser = g.user
        applied_job = await db.tracked_jobs.find_unique(where={"userId": currentUser.id, "id": jobId})
        if not applied_job:
            return jsonify({"success": False, "error": "Applied Job not exists"}), 400
        
        # Update the user to connect the job
        await db.tracked_jobs.update(
            where={"userId": currentUser.id, "id": jobId},
            data={
                "status": status
            }
        )
        
        return jsonify({"success": True, "message": "Job saved to user"}), 200
    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        await db.disconnect()


@user_blueprint.route('/job/bookmark', methods=['POST'])
async def bookmark_job():

    jobId = request.args.get('jobId', default=None, type=str)
    if not job:
        return jsonify({"success": False, "error": "Job not exists"}), 400

    # Find the job by its ID
    job = await db.job.find_unique(where={"id": jobId})
    if not job:
        return jsonify({"success": False, "error": "Job not exists"}), 404
    
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
    
    return jsonify({"success": True, "message": "Job saved to user"}), 200

@user_blueprint.route('/job/create', methods=['POST'])
async def create_job():
    try:
        await db.connect()
        body_data = request.get_json()
        print(body_data, "here is the body data")
        
        # Get the current user from the request context
        currentUser = g.user
        user = await db.user.find_unique(where={"id": currentUser.id})
        if not user:
            return jsonify({"success": False, "message": "User not exists"}), 400
        
        try:
            # Attempt to insert the job
            job = await insert_job(body_data)
            print(job, "here is the job")

            # If successful, create a tracked job entry
            await db.tracked_jobs.create(
                data={
                    "userId": currentUser.id,
                    "jobId": job.id,
                    "status": body_data.status
                }
            )
            return jsonify({"success": True, "message": "Job saved to user"}), 200

        except Exception as insert_error:
            print(insert_error, "error during job insertion")
            # If insert_job fails, create a user job entry
            await db.connect()
            await db.user_jobs.create(
                data={
                    "userId": currentUser.id,
                    "title": body_data.get('title').lower(),
                    "job_link": body_data.get('job_link'),
                    "companyId": body_data.get('companyId'),
                    "job_location": body_data.get('job_location'),
                    "job_type": body_data.get('job_type'),
                    "job_salary": body_data.get('job_salary'),
                    "source": body_data.get('source'),
                    "posted": body_data.get('posted', datetime.now().isoformat()),
                    "status": body_data.get('status')
                }
            )
            return jsonify({"success": True, "error": "User_job created"}), 500

    except Exception as e:
        print(e, "here is the error")  # Output the error to the console for debugging
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        await db.disconnect()

