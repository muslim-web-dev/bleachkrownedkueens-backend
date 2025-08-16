from functools import wraps
from flask import request, jsonify
import jwt
import os

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-this-in-production')

def token_required(f):
    """Decorator to require valid JWT token for routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user_id = data['user_id']
            current_username = data['username']
            
            # Pass user info to the route
            return f(current_user_id, current_username, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated

def decode_token(token):
    """Helper function to decode JWT token"""
    try:
        if not token:
            return None
            
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
            
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return {
            'user_id': data.get('user_id'),
            'username': data.get('username')
        }
    except:
        return None