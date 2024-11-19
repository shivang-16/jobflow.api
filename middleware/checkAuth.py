from flask import jsonify, request, g
import jwt
import os
from db.prisma import db

JWT_SECRET_TOKEN = os.getenv('JWT_SECRET')

async def checkAuth():
    try:
        await db.connect()
        token = request.cookies.get('token')
        print(token, "here")
        if not token:
            print("Unauthorised: Login First")
            return jsonify(({"error": "Unauthorised: Login First"}))
        
        payload = jwt.decode(token, JWT_SECRET_TOKEN, algorithms=['HS256'])
        
        user = await db.user.find_unique(where={'id': payload['userId']})

        if not user:
            return jsonify(({"error": "User not exists"}))

        g.user = user

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Unauthorized: Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Unauthorized: Invalid token'}), 401
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500
    finally:
        await db.disconnect()


async def protect_routes():
    auth_result = await checkAuth()  # Call the middleware
    if auth_result:
        print(auth_result)
        return auth_result  # If authentication fails, return the error response