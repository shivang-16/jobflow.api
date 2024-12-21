import os
from flask import jsonify, make_response
import jwt

JWT_SECRET_TOKEN = os.getenv('JWT_SECRET')

async def setCookie(user):
    payload = {
        'userId': user.id,
    }
    token = jwt.encode(payload, JWT_SECRET_TOKEN, algorithm='HS256')

    # Create a response object with a success message
    response = make_response(jsonify({'message': 'User created successfully', "token": token}), 201)

    # Set the cookie
    response.set_cookie(
        'token',
        value=token,
        httponly=True,
        secure=True,  # Use HTTPS in production
        samesite='None',  # Ensure cookies work in cross-site contexts
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        domain=".jobflow.in"
    )

    return response


