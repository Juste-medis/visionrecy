from app import db
from datetime import datetime

# 3. Modèle Écoles Partenaires (School)
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120))
    address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

# 4. Modèle Modules Éducatifs (EducationalModule)
class EducationalModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    module_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

# 5. Modèle Participation aux Modules (UserModule)
class UserModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('educational_module.id'), nullable=False)
    score = db.Column(db.Float)
    completed_at = db.Column(db.DateTime)

# 6. Modèle Événements de Recyclage (RecyclingEvent)
class RecyclingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    event_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

# 7. Modèle Notifications Événements (EventNotification)
class EventNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('recycling_event.id'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.now)
