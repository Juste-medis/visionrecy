
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from flask_restful_swagger import swagger
from flask_restful import Api
from flask_migrate import Migrate
from flask_mail import Mail, Message


jwt = JWTManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail = Mail(app)

    app.mail = mail

    # Autoriser toutes les origines
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    api = swagger.docs(Api(app), apiVersion='1.0',
                       description='Documentation de l\'api vision rec')

    # Configurer le logger
    logging.basicConfig(
        filename='logs/app.log',
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] - %(message)s'
    )
    # # Enregistrement des blueprints

    from app.routes.auth.auth_routes import LoginResource, RegisterResource, LogoutResource, PasswordResetRequestResource, PasswordResetConfirmResource, PasswordChangeResource
    from app.routes.main.main_routes import SingleUpload, WasteHistoryCall
    from app.routes.main.school_routes import CreateSchool, GetSchoolsResource, GetSchoolResource, UpdateSchoolResource, DeleteSchoolResource, GetEducationalModules, CreateEducationalModule, UpdateEducationalModule, GetEducationalModule, DeleteEducationalModule
    from app.routes.main.challenge_routes import CreateChallengeResource, GetChallengesResource, GetChallengeResource, UpdateChallengeResource, DeleteChallengeResource, CreateUserChallenge
    from app.routes.site import IndexRessource
    from app.routes.site import HealthRessource #, RawAnalyzeAi, RemoteAnalyzeAi

    # API endpoints
    api.add_resource(IndexRessource, '/api')
    api.add_resource(HealthRessource, '/health')
    # api.add_resource(RawAnalyzeAi, '/analyze')
    # api.add_resource(RemoteAnalyzeAi, '/remote/analyze')

    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(RegisterResource, '/auth/register')
    api.add_resource(LogoutResource, '/auth/logout')
    api.add_resource(PasswordResetRequestResource, '/auth/ressetpass')
    api.add_resource(PasswordResetConfirmResource,
                     '/auth/confirm/passwordchange')
    api.add_resource(PasswordChangeResource, '/auth/changepassword')

    api.add_resource(SingleUpload, '/waste/classify')
    api.add_resource(WasteHistoryCall, '/waste/history')

    api.add_resource(CreateSchool, '/schools/create')
    api.add_resource(GetSchoolsResource, '/schools')
    api.add_resource(GetSchoolResource, '/schools/<int:id>')
    api.add_resource(UpdateSchoolResource, '/schools/<int:id>/update')
    api.add_resource(DeleteSchoolResource, '/schools/<int:id>/delete')
    api.add_resource(CreateEducationalModule, '/modules/create')
    api.add_resource(GetEducationalModules, '/modules')
    api.add_resource(GetEducationalModule, '/modules/<int:id>')
    api.add_resource(UpdateEducationalModule, '/modules/<int:id>/update')
    api.add_resource(DeleteEducationalModule, '/modules/<int:id>/delete')

    api.add_resource(CreateChallengeResource, '/challenges/create')
    api.add_resource(GetChallengesResource, '/challenges')
    api.add_resource(GetChallengeResource, '/challenges/<int:id>')
    api.add_resource(UpdateChallengeResource, '/challenges/<int:id>/update')
    api.add_resource(DeleteChallengeResource, '/challenges/<int:id>/delete')
    api.add_resource(CreateUserChallenge, '/userchallenges/<int:id>/register')

    # Frontend landing page → serve the demo UI bundled in static/demo
    @app.route('/', methods=['GET'])
    def frontend_demo():
        return send_from_directory('static/templates', 'index.html')

    app.add_url_rule("/", endpoint="index")

    # Gestion des erreurs
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)

    # Création des tables de la base de données
    with app.app_context():
        db.create_all()
        migrate = Migrate(app, db)
 
    return app
