from flask import Blueprint, request, jsonify
from db.prisma import db  
import bcrypt

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/', methods=['POST'])
async def create_user():
    # await db.connect()
    data = request.get_json()
    
    # Validate input
    if 'email' not in data or 'name' not in data or 'password' not in data:
        return jsonify({'error': 'Email, name, and password are required'}), 400
    
    email = data['email']
    name = data['name']
    password = data['password']
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        # Create a new user with async Prisma
        user = await db.user.create(
            data={
                'email': email,
                'name': name,
                'password': hashed_password.decode('utf-8'),  # Store the hashed password as a string
            }
        )
        print(user, "here")
        return dict(user), 201
    
    except Exception as e:
        print(e)  # Output the error to the console for debugging
        return jsonify({'error': str(e)}), 500

