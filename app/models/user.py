# Modèle de données pour les utilisateurs
from app import db
from datetime import datetime
from enum import Enum


def load_user(user_id):
    return User.query.get(int(user_id))


class UserLevel(Enum):
    ROOT = "root"
    SUPERROOT = "superroot"
    STANDARD = "standard"
    SCHOOL = "school"

    def __str__(self):
        return self.value


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    level = db.Column(db.Enum(UserLevel),
                      default=UserLevel.STANDARD)
    created_at = db.Column(db.DateTime, default=datetime.now)
    password_reset_code = db.Column(db.String(6), nullable=True)
    password_reset_code_expiry = db.Column(db.DateTime, nullable=True)

class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token_type = db.Column(db.String(50))
    token_value = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)


class UserSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notifications_enabled = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(10), default='en')
    theme = db.Column(db.String(10), default='light')
    created_at = db.Column(db.DateTime, default=datetime.now)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(255))
    read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.now)
