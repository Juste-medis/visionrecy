from flask import request, current_app
from app.routes.main.utils import process_image
from app.models.waste import WasteHistory
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from flask_restful_swagger import swagger
from swagger_doc import upload_doc, history_doc
from flask_restful import Resource


def index():
    """Retourne un message de bienvenue."""
    return """hello"""


class SingleUpload(Resource):
    @jwt_required()
    @swagger.operation(**upload_doc)
    def post(self):
        if 'file' not in request.files:
            return {"success": False, "message": "Aucun fichier fourni"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"success": False, "message": "Aucun fichier sélectionné"}, 400

        # Traitement de l'image
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        predicted_class, confidence = process_image(file, filename)

        current_user = get_jwt_identity()

        # Enregistrement dans l'historique
        waste_history = WasteHistory(
            user_id=current_user,
            filename=file.filename,
            prediction=predicted_class,
            confidence=confidence
        )
        db.session.add(waste_history)
        db.session.commit()

        return {
            "success": True,
            "message": "Classification réussie",
            "prediction": predicted_class,
            "treatment": predicted_class,
            "confidence": confidence
        }, 200


class WasteHistoryCall(Resource):
    @jwt_required()
    @swagger.operation(**history_doc)
    def get(self):
        current_user = get_jwt_identity()
        waste_history = WasteHistory.query.filter_by(
            user_id=current_user).all()

        history_data = [{
            "id": entry.id,
            "filename": entry.filename,
            "prediction": entry.prediction,
            "confidence": entry.confidence,
            "timestamp": entry.timestamp.isoformat()
        } for entry in waste_history]

        return {"success": True, "history": history_data}, 200
