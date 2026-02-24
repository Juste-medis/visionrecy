# Gestionnaires d'erreurs
from flask import jsonify, request, send_from_directory

def register_error_handlers(app):
    def _wants_json():
        # Favor JSON for API-style calls; otherwise serve the branded HTML page.
        return request.is_json or request.path.startswith("/api") or request.accept_mimetypes.best == "application/json"

    @app.errorhandler(400)
    def bad_request(error):
        if _wants_json():
            return jsonify({"success": False, "message": "Requete invalide"}), 400
        return send_from_directory('static/templates', '400.html'), 400

    @app.errorhandler(401)
    def unauthorized(error):
        if _wants_json():
            return jsonify({"success": False, "message": "Non autorise"}), 401
        return send_from_directory('static/templates', '401.html'), 401

    @app.errorhandler(404)
    def not_found(error):
        if _wants_json():
            return jsonify({"success": False, "message": "Ressource non trouvee"}), 404
        return send_from_directory('static/templates', '404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        if _wants_json():
            return jsonify({"success": False, "message": "Erreur interne du serveur"}), 500
        return send_from_directory('static/templates', '500.html'), 500