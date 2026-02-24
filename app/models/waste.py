# Modèle de données pour l'historique des déchets
from app import db
from datetime import datetime

class WasteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Clé étrangère vers User
    filename = db.Column(db.String(100), nullable=False)  # Nom du fichier image
    prediction = db.Column(db.String(50), nullable=False)  # Catégorie prédite
    confidence = db.Column(db.Float, nullable=False)  # Pourcentage de confiance
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Date et heure de la prédiction

class WasteStatistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    total_uploads = db.Column(db.Integer, nullable=False) 
    plastic_count = db.Column(db.Integer, nullable=False) 
    glass_count = db.Column(db.Integer, nullable=False) 
    paper_count = db.Column(db.Integer, nullable=False) 
    metal_count = db.Column(db.Integer, nullable=False) 
    organic_count = db.Column(db.Integer, nullable=False) 
    automobile_count = db.Column(db.Integer, nullable=False) 
    lamp_count = db.Column(db.Integer, nullable=False) 
    battery_count = db.Column(db.Integer, nullable=False) 
    electronic_count = db.Column(db.Integer, nullable=False) 
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now) 

 