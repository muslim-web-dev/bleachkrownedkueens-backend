from src.models.user import db
from datetime import datetime, timedelta

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('password_resets', lazy=True))
    
    def __init__(self, user_id, email, otp_code):
        self.user_id = user_id
        self.email = email
        self.otp_code = otp_code
        self.expires_at = datetime.utcnow() + timedelta(minutes=15)  # OTP expires in 15 minutes
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        return not self.is_used and not self.is_expired() and self.attempts < 3
    
    def increment_attempts(self):
        self.attempts += 1
        db.session.commit()
    
    def mark_as_used(self):
        self.is_used = True
        db.session.commit()
    
    @staticmethod
    def cleanup_expired():
        """Remove expired OTP codes"""
        expired = PasswordReset.query.filter(
            PasswordReset.expires_at < datetime.utcnow()
        ).delete()
        db.session.commit()
        return expired