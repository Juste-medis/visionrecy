from flask import request,current_app
from flask_restful import Resource
from flask_restful_swagger import swagger
from flask_jwt_extended import create_access_token

from app.routes.auth.utils import validate_login, validate_registration,validate_password_reset_request,validate_password_reset_confirm
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
from datetime import datetime, timedelta

from app import db
from swagger_doc import login_doc, register_doc, logout_doc,password_reset_request_doc, password_reset_confirm_doc,password_change_doc
from itsdangerous import URLSafeTimedSerializer
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash 

from flask_mail import Message
  

class LoginResource(Resource):
    @swagger.operation(**login_doc)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user, error = validate_login(email, password)
        if error:
            return {"success": False, "message": error}, 400

        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.username,
        }
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=user_data,
            expires_delta=timedelta(days=15)
        )
        return {
            "access_token": access_token,
            "success": True,
            "message": "Connexion réussie",
            "user_id": user.id,
        }, 200


class RegisterResource(Resource):
    @swagger.operation(**register_doc)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user, error = validate_registration(username, email, password)
        if error:
            return {"success": False, "message": error}, 400

        db.session.add(user)
        db.session.commit()

        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.username,
        }
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=user_data,
            expires_delta=timedelta(days=15)
        )
        return {
            "access_token": access_token,
            "success": True,
            "message": "Inscription réussie",
            "user_id": user.id,
        }, 201


class LogoutResource(Resource):
    @swagger.operation(**logout_doc)
    def post(self):
        return {"success": True, "message": "Déconnexion réussie"}, 200
    
    
class PasswordResetRequestResource(Resource):
    @swagger.operation(**password_reset_request_doc)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        
        error = validate_password_reset_request(email)
        if error:
            return {"success": False, "message": error}, 400
        
        user = User.query.filter_by(email=email).first()
        
        # Générer un code à 6 chiffres
        reset_code ='123456'# ''.join([str(random.randint(0, 9)) for _ in range(6)])
        reset_code_expiry = datetime.utcnow() + timedelta(minutes=30)  # Expire dans 30 minutes
        
        # Stocker le code dans la base de données
        user.password_reset_code = reset_code
        user.password_reset_code_expiry = reset_code_expiry
        db.session.commit()
        
        # Envoyer le code par email
        msg = Message(
            "Code de réinitialisation de mot de passe",
            recipients=[email],
            body=f"Votre code de réinitialisation est : {reset_code}\n"
                 f"Ce code expirera dans 30 minutes."
        )
        # current_app.mail.send(msg)
        
        return {
            "success": True,
            "message": "Code de réinitialisation envoyé par email",
        }, 200


class PasswordResetConfirmResource(Resource):
    @swagger.operation(**password_reset_confirm_doc)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        reset_code = data.get('reset_code')
        new_password = data.get('new_password')
        
        user = User.query.filter_by(email=email).first()
        
        # Vérifier le code
        if (not user or 
            not user.password_reset_code or 
            user.password_reset_code != reset_code or
            user.password_reset_code_expiry < datetime.utcnow()):
            return {
                "success": False,
                "message": "Code invalide ou expiré"
            }, 400
        
        user, error = validate_password_reset_confirm(email, new_password)
        if error:
            return {"success": False, "message": error}, 400
        
        # Mettre à jour le mot de passe et effacer le code
        user.password = generate_password_hash(new_password)
        user.password_reset_code = None
        user.password_reset_code_expiry = None
        db.session.commit()
        
        return {
            "success": True,
            "message": "Mot de passe réinitialisé avec succès"
        }, 200


class PasswordChangeResource(Resource):
    # (Ceci reste inchangé car il ne concerne pas la réinitialisation)
    @swagger.operation(**password_change_doc)
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_password = data.get('password')
        new_password = data.get('new_password')
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.check_password(current_password):
            return {
                "success": False,
                "message": "Mot de passe actuel incorrect"
            }, 400
        
        error = validate_password_reset_confirm(user.email, new_password)
        if error:
            return {"success": False, "message": error}, 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return {
            "success": True,
            "message": "Mot de passe changé avec succès"
        }, 200