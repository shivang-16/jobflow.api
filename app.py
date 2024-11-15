from flask import Flask
from prisma import register
from controllers.auth import user_blueprint
from controllers.job import job_blueprint
from db.prisma import db
from flask_cors import CORS


app = Flask(__name__)

CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Register Prisma with Flask
register(db)

# Function to ensure the database connection



@app.route('/')
def hello_world():
    return 'Hello world'

# Register your blueprints
app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(job_blueprint, url_prefix='/api/job')

if __name__ == '__main__':
    app.run(debug=True)
