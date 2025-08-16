from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.models.user import db, User
from src.models.password_reset import PasswordReset
import jwt
import os
import random
import string
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth_bp = Blueprint('auth', __name__)

# Secret key for JWT (in production, use environment variable)
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-this-in-production')

# Email configuration (use environment variables in production)
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'nexgen.times01@gmail.com')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'ijpx osnf yotq kikt')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'nexgen.times01@gmail.com')

@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                return jsonify({'error': 'Username already taken'}), 409
            else:
                return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': new_user.id,
            'username': new_user.username,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
@cross_origin()
def verify_token():
    """Verify JWT token"""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        # Extract token from "Bearer <token>" format
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        # Decode token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload['user_id']
            
            # Get user info
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'valid': True,
                'user': user.to_dict()
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    """Logout user (client-side token removal)"""
    # In a more complex system, you might want to blacklist the token
    # For now, just return success and let client remove the token
    return jsonify({'message': 'Logged out successfully'}), 200

def generate_otp():
    """Generate a 6-digit OTP code"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp_code):
    """Send OTP code via email"""
    try:
        # If SMTP credentials not configured, print to console (dev mode)
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            print(f"\n[DEV MODE] OTP for {email}: {otp_code}\n")
            return True
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Password Reset Code - Krowned Kueens'
        msg['From'] = FROM_EMAIL
        msg['To'] = email
        
        # Create the HTML content
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #1a1a1a; color: #ffffff; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #2a2a2a; border-radius: 10px; padding: 30px;">
              <h1 style="color: #ff1493; text-align: center;">KROWNED KUEENS</h1>
              <h2 style="color: #ffffff; text-align: center;">Password Reset Code</h2>
              <p style="color: #cccccc; text-align: center;">Your one-time password reset code is:</p>
              <div style="background-color: #333333; border: 2px solid #ff1493; border-radius: 5px; padding: 20px; margin: 20px 0; text-align: center;">
                <span style="font-size: 32px; font-weight: bold; color: #ff1493; letter-spacing: 5px;">{otp_code}</span>
              </div>
              <p style="color: #cccccc; text-align: center;">This code will expire in 15 minutes.</p>
              <p style="color: #999999; text-align: center; font-size: 12px;">If you didn't request this code, please ignore this email.</p>
            </div>
          </body>
        </html>
        """
        
        # Attach HTML content
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        # In development, still print the OTP
        print(f"\n[EMAIL ERROR] OTP for {email}: {otp_code}\n")
        return True  # Return True to allow testing without email

@auth_bp.route('/forgot-password', methods=['POST'])
@cross_origin()
def forgot_password():
    """Send OTP code for password reset"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists or not for security
            return jsonify({'message': 'If the email exists, a reset code has been sent'}), 200
        
        # Clean up any expired OTP codes
        PasswordReset.cleanup_expired()
        
        # Check if there's a recent OTP request (rate limiting)
        recent_reset = PasswordReset.query.filter_by(
            user_id=user.id,
            is_used=False
        ).filter(
            PasswordReset.created_at > datetime.utcnow() - timedelta(minutes=2)
        ).first()
        
        if recent_reset:
            return jsonify({'error': 'Please wait 2 minutes before requesting another code'}), 429
        
        # Generate OTP code
        otp_code = generate_otp()
        
        # Store OTP in database
        password_reset = PasswordReset(
            user_id=user.id,
            email=email,
            otp_code=otp_code
        )
        db.session.add(password_reset)
        db.session.commit()
        
        # Send OTP via email
        send_otp_email(email, otp_code)
        
        return jsonify({
            'message': 'If the email exists, a reset code has been sent',
            'email': email  # Return email for frontend to use
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Forgot password error: {e}")
        return jsonify({'error': 'Failed to process request'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
@cross_origin()
def verify_otp():
    """Verify OTP code and reset password"""
    try:
        data = request.get_json()
        email = data.get('email')
        otp_code = data.get('otp')
        new_password = data.get('password')
        
        if not email or not otp_code:
            return jsonify({'error': 'Email and OTP code are required'}), 400
        
        # Find the most recent valid OTP for this email
        password_reset = PasswordReset.query.filter_by(
            email=email,
            otp_code=otp_code,
            is_used=False
        ).order_by(PasswordReset.created_at.desc()).first()
        
        if not password_reset:
            return jsonify({'error': 'Invalid or expired OTP code'}), 400
        
        # Check if OTP is valid
        if not password_reset.is_valid():
            if password_reset.is_expired():
                return jsonify({'error': 'OTP code has expired'}), 400
            elif password_reset.attempts >= 3:
                return jsonify({'error': 'Too many failed attempts'}), 400
            else:
                return jsonify({'error': 'Invalid OTP code'}), 400
        
        # Increment attempts
        password_reset.increment_attempts()
        
        # If new password provided, reset it
        if new_password:
            user = User.query.get(password_reset.user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Update password
            user.set_password(new_password)
            
            # Mark OTP as used
            password_reset.mark_as_used()
            
            db.session.commit()
            
            return jsonify({
                'message': 'Password reset successful',
                'success': True
            }), 200
        else:
            # Just verify OTP without resetting password
            return jsonify({
                'message': 'OTP verified successfully',
                'valid': True
            }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Verify OTP error: {e}")
        return jsonify({'error': 'Failed to verify OTP'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
@cross_origin()
def reset_password():
    """Reset password with verified OTP"""
    try:
        data = request.get_json()
        email = data.get('email')
        otp_code = data.get('otp')
        new_password = data.get('password')
        
        if not email or not otp_code or not new_password:
            return jsonify({'error': 'Email, OTP, and new password are required'}), 400
        
        # Verify OTP and reset password
        return verify_otp()
    except Exception as e:
        return jsonify({'error': str(e)}), 500