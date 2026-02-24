from app import db
from datetime import datetime


# 6. Défis (Challenge)
class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    reward_points = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)
    goal = db.Column(db.Float, default=100)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now) 

# 7. Participation aux Défis (UserChallenge)
class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    progress = db.Column(db.Float) 
    completed_at = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now) 
