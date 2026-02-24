from flask import request, jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger
from app import db
from app.models.challenge import Challenge, UserChallenge
from swagger_doc import (
    create_challenge_doc, get_challenges_doc, get_challenge_doc,
    update_challenge_doc, delete_challenge_doc, create_cuserhallenge_doc
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.utils.myshemas import validate_data, get_challenge_shema, get_userchallenge_shema


class CreateChallengeResource(Resource):
    @jwt_required()
    @swagger.operation(**create_challenge_doc)
    def post(self):
        try:
            data = request.get_json()
            is_valid, error = validate_data(data, get_challenge_shema())
            if not is_valid:
                return {"success": False, "message": error}, 400

            start_date = datetime.strptime(
                data['start_date'], "%Y-%m-%d")
            expiration_date = datetime.strptime(
                data['expiration_date'], "%Y-%m-%d")
            if start_date >= expiration_date:
                return {'error': "La date de fin doit être postérieure à la date de début."}, 400

            new_challenge = Challenge(**data)

            db.session.add(new_challenge)
            db.session.commit()
            return {'message': 'Challenge créé avec succès'}, 201
        except Exception as e:
            return {'error': str(e)}, 400


class GetChallengesResource(Resource):
    @swagger.operation(**get_challenges_doc)
    def get(self):
        challenges = Challenge.query.all()
        return [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'reward_points': c.reward_points,
            'goal': c.goal,
            'start_date': c.start_date.strftime('%Y-%m-%d'),
            'expiration_date': c.expiration_date.strftime('%Y-%m-%d')
        } for c in challenges], 200


class GetChallengeResource(Resource):
    @swagger.operation(**get_challenge_doc)
    def get(self, challenge_id):
        challenge = Challenge.query.get_or_404(challenge_id)
        return {
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'reward_points': challenge.reward_points,
            'goal': challenge.goal,
            'start_date': challenge.start_date.strftime('%Y-%m-%d'),
            'expiration_date': challenge.expiration_date.strftime('%Y-%m-%d')
        }, 200


class UpdateChallengeResource(Resource):
    @jwt_required()
    @swagger.operation(**update_challenge_doc)
    def put(self, challenge_id):
        challenge = Challenge.query.get_or_404(challenge_id)
        try:
            data = request.get_json()
            validated_data = validate_data(data)

            is_valid, error = validate_data(
                data, get_challenge_shema(is_update=True))
            if not is_valid:
                return {"success": False, "message": error}, 400

            start_date = datetime.strptime(
                validated_data['start_date'], "%Y-%m-%d")
            expiration_date = datetime.strptime(
                validated_data['expiration_date'], "%Y-%m-%d")
            if start_date >= expiration_date:
                return {'error': "La date de fin doit être postérieure à la date de début."}, 400

            challenge.title = validated_data['title']
            challenge.description = validated_data['description']
            challenge.reward_points = validated_data['reward_points']
            challenge.goal = validated_data['goal']
            challenge.start_date = start_date
            challenge.expiration_date = expiration_date
            db.session.commit()
            return {'message': 'Challenge mis à jour avec succès'}, 200
        except Exception as e:
            return {'error': str(e)}, 400


class DeleteChallengeResource(Resource):
    @jwt_required()
    @swagger.operation(**delete_challenge_doc)
    def delete(self, challenge_id):
        challenge = Challenge.query.get_or_404(challenge_id)
        db.session.delete(challenge)
        db.session.commit()
        return {'message': 'Challenge supprimé avec succès'}, 200


class CreateUserChallenge(Resource):
    @jwt_required()
    @swagger.operation(**create_cuserhallenge_doc)
    def post(self):
        try:
            data = request.get_json()
            is_valid, error = validate_data(data, get_userchallenge_shema())
            if not is_valid:
                return {"success": False, "message": error}, 400

            #  Vérifier si l'école associée existe
            challenge = Challenge.query.get(data['challenge_id'])
            if not challenge:
                return {"success": False, "message": "Challenge introuvable."}, 404

            #  Vérifier si l'école associée existe
            theuser = Challenge.query.get(data['challenge_id'])
            if not theuser:
                return {"success": False, "message": "Utilisateur introuvable."}, 404

            new_challenge = UserChallenge(**data)

            db.session.add(new_challenge)
            db.session.commit()
            return {'message': 'Inscription réuissi', "success": True, }, 201
        except Exception as e:
            return {'error': str(e)}, 400
0