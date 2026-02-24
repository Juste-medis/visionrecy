from flask import request
from schema import Schema, And, Optional
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger
from app import db
from app.models.school import School, EducationalModule
from swagger_doc import create_school_doc, get_schools_doc, get_school_doc, update_school_doc, delete_school_doc, create_module, get_modules, get_module, modify_module, delete_module

from app.utils.myshemas import validate_data, getschool_schema, get_module_schema
from flask_jwt_extended import jwt_required, get_jwt_identity


class CreateSchool(Resource):
    @jwt_required()
    @swagger.operation(**create_school_doc)
    def post(self):
        data = request.get_json()
        school_data = {
            'name': data.get('name'),
            'contact_email': data.get('contact_email'),
            'address': data.get('address'),
        }

        is_valid, error = validate_data(school_data, getschool_schema("c"))
        if not is_valid:
            return {"success": False, "message": error}, 400

        new_school = School(**school_data)
        db.session.add(new_school)
        db.session.commit()

        return {
            "success": True,
            "message": "École créée avec succès",
            "school": {
                "id": new_school.id,
                "name": new_school.name,
                "contact_email": new_school.contact_email,
                "address": new_school.address,
                "created_at": new_school.created_at.isoformat() if new_school.created_at else None
            }
        }, 201


class GetSchoolsResource(Resource):
    @swagger.operation(**get_schools_doc)
    def get(self):
        schools = School.query.all()
        return [{
            'id': school.id,
            'name': school.name,
            'contact_email': school.contact_email,
            'address': school.address
        } for school in schools], 200


class GetSchoolResource(Resource):
    @swagger.operation(**get_school_doc)
    def get(self, id):
        school = School.query.get_or_404(id)
        return {
            'id': school.id,
            'name': school.name,
            'contact_email': school.contact_email,
            'address': school.address
        }, 200


class UpdateSchoolResource(Resource):
    @jwt_required()
    @swagger.operation(**update_school_doc)  # Swagger documentation (optional)
    def put(self, id):
        # Récupérer l'école par son ID ou retourner une erreur 404 si non trouvée
        school = School.query.get_or_404(id)

        # Récupérer les données JSON de la requête
        data = request.get_json()

        # Préparer les données pour la validation
        school_data = {
            'name': data.get('name'),
            'contact_email': data.get('contact_email'),
            'address': data.get('address'),
        }

        # Valider les données
        is_valid, error = validate_data(school_data, getschool_schema("u"))
        if not is_valid:
            return {"success": False, "message": error}, 400

        if 'name' in data:
            school.name = data['name']
        if 'contact_email' in data:
            school.contact_email = data['contact_email']
        if 'address' in data:
            school.address = data['address']

        db.session.commit()

        # Retourner une réponse de succès
        return {
            "success": True,
            "message": "École mise à jour avec succès",
            "school": {
                "id": school.id,
                "name": school.name,
                "contact_email": school.contact_email,
                "address": school.address,
                "created_at": school.created_at.isoformat() if school.created_at else None
            }
        }, 200


class DeleteSchoolResource(Resource):
    @jwt_required()
    @swagger.operation(**delete_school_doc)
    def delete(self, id):
        school = School.query.get_or_404(id)
        db.session.delete(school)
        db.session.commit()
        return {'message': 'École supprimée avec succès'}, 200

# Education modules


class CreateEducationalModule(Resource):
    @jwt_required()
    @swagger.operation(**create_module)
    def post(self):
        data = request.get_json()

        # Validation des données
        is_valid, error = validate_data(data, get_module_schema("c"))
        if not is_valid:
            return {"success": False, "message": error}, 400

        #  Vérifier si l'école associée existe
        school = School.query.get(data['school_id'])
        if not school:
            return {"success": False, "message": "École introuvable."}, 404

        # Création du module
        new_module = EducationalModule(**data)
        db.session.add(new_module)
        db.session.commit()

        return {
            "success": True,
            "message": "Module éducatif créé avec succès",
            "module": {
                "id": new_module.id,
                "school_id": new_module.school_id,
                "title": new_module.title,
                "description": new_module.description,
                "module_type": new_module.module_type,
                "created_at": new_module.created_at.isoformat()
            }
        }, 201


class GetEducationalModules(Resource):
    @swagger.operation(**get_modules)
    def get(self):
        modules = EducationalModule.query.all()
        return [{
            'id': module.id,
            'school_id': module.school_id,
            'title': module.title,
            'description': module.description,
            'module_type': module.module_type,
            'created_at': module.created_at.isoformat()
        } for module in modules], 200


class GetEducationalModule(Resource):
    @swagger.operation(**get_module)
    def get(self, id):
        module = EducationalModule.query.get_or_404(id)
        return {
            'id': module.id,
            'school_id': module.school_id,
            'title': module.title,
            'description': module.description,
            'module_type': module.module_type,
            'created_at': module.created_at.isoformat()
        }, 200


class UpdateEducationalModule(Resource):
    @jwt_required()
    @swagger.operation(**modify_module)
    def put(self, id):
        module = EducationalModule.query.get_or_404(id)
        data = request.get_json()

        is_valid, error = validate_data(data, get_module_schema("u"))
        if not is_valid:
            return {"success": False, "message": error}, 400

        if 'title' in data:
            module.title = data['title']
        if 'description' in data:
            module.description = data['description']
        if 'module_type' in data:
            module.module_type = data['module_type']

        db.session.commit()

        return {
            "success": True,
            "message": "Module mis à jour avec succès",
            "module": {
                "id": module.id,
                "school_id": module.school_id,
                "title": module.title,
                "description": module.description,
                "module_type": module.module_type,
                "created_at": module.created_at.isoformat()
            }
        }, 200


class DeleteEducationalModule(Resource):
    @jwt_required()
    @swagger.operation(**delete_module)
    def delete(self, id):
        module = EducationalModule.query.get_or_404(id)
        db.session.delete(module)
        db.session.commit()
        return {'message': 'Module éducatif supprimé avec succès'}, 200
