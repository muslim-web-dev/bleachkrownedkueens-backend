import os
import sys
import uuid
import time
import random
from datetime import datetime, timedelta
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_cors import CORS
from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.middleware.auth import decode_token

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, origins="*")

# Initialize SocketIO with simple configuration for deployment
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet'  # change from 'threading' to 'eventlet'
)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Global state management
connected_users = {}  # socket_id -> user_info
waiting_queue = []    # users waiting for matches
active_rooms = {}     # room_id -> room_info
user_reports = {}     # user_id -> report_count
banned_users = set()  # banned user IDs

# Simple user presence system
class UserPresenceSystem:
    @staticmethod
    def get_online_count():
        """Get real-time count of online users"""
        return len(connected_users)
    
    @staticmethod
    def add_user(socket_id, user_info):
        """Add user to online presence"""
        connected_users[socket_id] = {
            **user_info,
            'connected_at': datetime.now(),
            'last_activity': datetime.now()
        }
    
    @staticmethod
    def remove_user(socket_id):
        """Remove user from online presence"""
        if socket_id in connected_users:
            user_info = connected_users[socket_id]
            # Remove from waiting queue if present
            waiting_queue[:] = [u for u in waiting_queue if u['socket_id'] != socket_id]
            del connected_users[socket_id]
            return user_info
        return None

# Simple matching system
class MatchmakingSystem:
    @staticmethod
    def find_match(user_info):
        """Find the best match for a user"""
        if not waiting_queue:
            return None
        
        # Simple random matching for now
        for i, waiting_user in enumerate(waiting_queue):
            if waiting_user['user_id'] != user_info['user_id']:
                waiting_queue.pop(i)
                return waiting_user
        
        return None
    
    @staticmethod
    def create_room(user1, user2):
        """Create a new chat room for two users"""
        room_id = str(uuid.uuid4())
        room_info = {
            'id': room_id,
            'users': [user1, user2],
            'created_at': datetime.now(),
            'messages': []
        }
        active_rooms[room_id] = room_info
        return room_id

# REST API Endpoints
@app.route('/')
def welcome():
    return "Welcome to my Flask API V0.0.1"

@app.route('/api/stats')
def get_stats():
    """Get platform statistics"""
    return jsonify({
        'online_users': UserPresenceSystem.get_online_count(),
        'active_rooms': len(active_rooms),
        'waiting_users': len(waiting_queue)
    })

@app.route('/api/report', methods=['POST'])
def report_user():
    """Report a user for inappropriate behavior"""
    data = request.json
    reporter_id = data.get('reporter_id')
    reported_id = data.get('reported_id')
    reason = data.get('reason', 'Inappropriate behavior')
    
    if not reporter_id or not reported_id:
        return jsonify({'error': 'Missing required fields'}), 400
    
    return jsonify({
        'success': True,
        'message': 'User reported successfully'
    })

# WebRTC Signaling Events
@socketio.on('connect')
def handle_connect(auth):
    """Handle user connection with authentication"""
    print(f'Socket connected: {request.sid}')
    
    # Try to get user from auth token
    user_info = None
    if auth and 'token' in auth:
        user_info = decode_token(auth['token'])
    
    if user_info:
        print(f'Authenticated user connected: {user_info["username"]}')
        # Store authenticated user info with socket
        connected_users[request.sid] = {
            'socket_id': request.sid,
            'user_id': user_info['user_id'],
            'username': user_info['username'],
            'authenticated': True,
            'connected_at': datetime.now(),
            'last_activity': datetime.now()
        }
    
    emit('connected', {'socket_id': request.sid, 'authenticated': bool(user_info)})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection"""
    print(f'User disconnected: {request.sid}')
    user_info = UserPresenceSystem.remove_user(request.sid)
    
    if user_info:
        # Notify partner if in a room
        for room_id, room_info in list(active_rooms.items()):
            if any(u['socket_id'] == request.sid for u in room_info['users']):
                # Find partner
                partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
                if partner:
                    emit('partner_disconnected', room=partner['socket_id'])
                # Clean up room
                del active_rooms[room_id]
                break
    
    # Broadcast updated user count
    socketio.emit('user_count_update', {'count': UserPresenceSystem.get_online_count()})

@socketio.on('join_platform')
def handle_join_platform(data):
    """Handle user joining the platform"""
    # Check if user is already authenticated from connection
    if request.sid in connected_users:
        user_info = connected_users[request.sid]
        user_info['interests'] = data.get('interests', [])
        user_info['status'] = 'online'
    else:
        # Fallback for non-authenticated users
        user_id = data.get('user_id', str(uuid.uuid4()))
        username = data.get('username', f'Guest_{user_id[:8]}')
        
        user_info = {
            'socket_id': request.sid,
            'user_id': user_id,
            'username': username,
            'interests': data.get('interests', []),
            'status': 'online',
            'authenticated': False,
            'connected_at': datetime.now(),
            'last_activity': datetime.now()
        }
        
        UserPresenceSystem.add_user(request.sid, user_info)
    
    emit('joined_platform', {
        'user_id': user_info['user_id'],
        'username': user_info.get('username'),
        'online_count': UserPresenceSystem.get_online_count()
    })
    
    # Broadcast updated user count
    socketio.emit('user_count_update', {'count': UserPresenceSystem.get_online_count()})

@socketio.on('find_match')
def handle_find_match(data):
    """Handle user requesting to find a match"""
    if request.sid not in connected_users:
        emit('error', {'message': 'Not connected to platform'})
        return
    
    user_info = connected_users[request.sid]
    interests = data.get('interests', [])
    user_info['interests'] = interests
    
    # Check if user is already in queue
    for queued_user in waiting_queue:
        if queued_user['socket_id'] == request.sid:
            emit('error', {'message': 'Already searching for a match'})
            return
    
    # Try to find immediate match
    match = MatchmakingSystem.find_match(user_info)
    
    if match:
        # Verify matched user is still connected
        if match['socket_id'] not in connected_users:
            # User disconnected, continue searching
            waiting_queue.append(user_info)
            emit('searching', {'message': 'Looking for a match...'})
            return
            
        # Create room and connect users
        room_id = MatchmakingSystem.create_room(user_info, match)
        
        # Join both users to the room
        join_room(room_id, sid=request.sid)
        join_room(room_id, sid=match['socket_id'])
        
        # Notify current user (initiator = true)
        emit('match_found', {
            'room_id': room_id,
            'partner': {
                'user_id': match['user_id'],
                'username': match.get('username', 'Anonymous'),
                'interests': match.get('interests', []),
                'authenticated': match.get('authenticated', False)
            },
            'initiator': True  # This user creates the offer
        })
        
        # Notify matched user (initiator = false)
        emit('match_found', {
            'room_id': room_id,
            'partner': {
                'user_id': user_info['user_id'],
                'username': user_info.get('username', 'Anonymous'),
                'interests': user_info.get('interests', []),
                'authenticated': user_info.get('authenticated', False)
            },
            'initiator': False  # This user waits for offer
        }, room=match['socket_id'])
        
    else:
        # Add to waiting queue
        waiting_queue.append(user_info)
        emit('searching', {'message': 'Looking for a match...'})

@socketio.on('cancel_search')
def handle_cancel_search():
    """Handle user canceling search"""
    # Remove from waiting queue
    waiting_queue[:] = [u for u in waiting_queue if u['socket_id'] != request.sid]
    emit('search_cancelled')

@socketio.on('webrtc_offer')
def handle_webrtc_offer(data):
    """Handle WebRTC offer"""
    room_id = data.get('room_id')
    offer = data.get('offer')
    
    if room_id in active_rooms:
        # Forward offer to partner
        room_info = active_rooms[room_id]
        partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
        
        if partner:
            emit('webrtc_offer', {
                'offer': offer,
                'from': request.sid
            }, room=partner['socket_id'])

@socketio.on('webrtc_answer')
def handle_webrtc_answer(data):
    """Handle WebRTC answer"""
    room_id = data.get('room_id')
    answer = data.get('answer')
    
    if room_id in active_rooms:
        # Forward answer to partner
        room_info = active_rooms[room_id]
        partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
        
        if partner:
            emit('webrtc_answer', {
                'answer': answer,
                'from': request.sid
            }, room=partner['socket_id'])

@socketio.on('webrtc_ice_candidate')
def handle_ice_candidate(data):
    """Handle ICE candidate"""
    room_id = data.get('room_id')
    candidate = data.get('candidate')
    
    if room_id in active_rooms:
        # Forward ICE candidate to partner
        room_info = active_rooms[room_id]
        partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
        
        if partner:
            emit('webrtc_ice_candidate', {
                'candidate': candidate,
                'from': request.sid
            }, room=partner['socket_id'])

@socketio.on('send_message')
def handle_send_message(data):
    """Handle chat message"""
    room_id = data.get('room_id')
    message = data.get('message')
    username = data.get('username')
    print(data)
    
    if room_id in active_rooms and message:
        room_info = active_rooms[room_id]
        user_info = connected_users.get(request.sid)
        
        if user_info:
            # Get username from message data first, then from user_info, then use default
            username = user_info.get('username', f"User{user_info.get('user_id', 'Unknown')}")
            
            print(f"[CHAT] User {username} (ID: {user_info['user_id']}) sending message")
            
            message_data = {
                'id': str(uuid.uuid4()),
                'user_id': user_info['user_id'],
                'username': username,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"[CHAT] Message data: {message_data}")
            
            # Store message in room
            room_info['messages'].append(message_data)
            
            # Send to both users with proper sender identification
            # To sender: mark as 'you'
            sender_message = message_data.copy()
            sender_message['sender'] = 'you'
            emit('message_sent', sender_message)
            
            # To partner: mark as 'partner' but keep the username
            partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
            if partner:
                partner_message = message_data.copy()
                partner_message['sender'] = 'partner'
                emit('receive_message', partner_message, room=partner['socket_id'])

@socketio.on('skip_partner')
def handle_skip_partner(data):
    """Handle user skipping current partner"""
    room_id = data.get('room_id')
    
    if room_id in active_rooms:
        room_info = active_rooms[room_id]
        
        # Notify partner
        partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
        if partner:
            emit('partner_skipped', room=partner['socket_id'])
            leave_room(room_id, sid=partner['socket_id'])
        
        # Leave room
        leave_room(room_id, sid=request.sid)
        
        # Clean up room
        del active_rooms[room_id]
        
        emit('skipped')

@socketio.on('end_chat')
def handle_end_chat(data):
    """Handle user ending chat"""
    room_id = data.get('room_id')
    
    if room_id in active_rooms:
        room_info = active_rooms[room_id]
        
        # Notify partner
        partner = next((u for u in room_info['users'] if u['socket_id'] != request.sid), None)
        if partner:
            emit('chat_ended', room=partner['socket_id'])
            leave_room(room_id, sid=partner['socket_id'])
        
        # Leave room
        leave_room(room_id, sid=request.sid)
        
        # Clean up room
        del active_rooms[room_id]
        
        emit('chat_ended')

# Serve frontend files (but not API routes)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Don't serve API routes through static file handler
    if path.startswith('api/'):
        return "Not Found", 404
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)  # local dev

