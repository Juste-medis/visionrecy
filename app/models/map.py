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

class RecyclingCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    title = db.Column(db.String(50), nullable=False)  # Catégorie prédite
    description = db.Column(db.String(100))
    address = db.Column(db.String(150))
    city = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    lat = db.Column(db.Float )  
    lon = db.Column(db.Float )   
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now) 

# 4. Centres de Recyclage (RecyclingCenter)
class RecyclingCenter(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(150))
    city = db.Column(db.String(50))
    contact = db.Column(db.String(20))
