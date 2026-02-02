from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from authlib.integrations.flask_client import OAuth

app = FastAPI()

class Data(BaseModel):
    name:str

@app.post("/create/")
async def create(data: Data):
    return {"data":data}


@app.get("/test/")
async def read_test():
    return {"message": "Test endpoint is working!"}

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# In-memory user storage (for demonstration purposes)
users = {}

# Initialize OAuth
oauth = OAuth(app)

# Configure OAuth2.0 provider (example: Google)
app.config['GOOGLE_CLIENT_ID'] = 'your_google_client_id'
app.config['GOOGLE_CLIENT_SECRET'] = 'your_google_client_secret'
app.config['GOOGLE_DISCOVERY_URL'] = (
    'https://accounts.google.com/.well-known/openid-configuration'
)

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
    client_kwargs={
        'scope': 'openid email profile',
    },
)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users.get(data['username'])
            if not current_user:
                raise ValueError('User not found')
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'message': 'User already exists!'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    users[username] = {'password': hashed_password}

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password!'}), 401

    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})

@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Welcome {current_user} to the protected route!'})

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google')
def google_auth():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    if user_info:
        username = user_info['email']
        if username not in users:
            users[username] = {'email': user_info['email'], 'name': user_info['name']}
        return jsonify({'message': f'Welcome {user_info["name"]}!', 'user': user_info})
    return jsonify({'message': 'Authentication failed!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
