from flask import request, current_app
from flask_restful import Resource
from flask_restful_swagger import swagger
from werkzeug.utils import secure_filename
from flask import render_template
import io
import logging

from app.routes.main.llava_processor import llava_analyzer
from PIL import Image

from app import db
from swagger_doc import login_doc

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexRessource(Resource): 
    def get(self):
        return render_template('index.html')


class HealthRessource(Resource): 
    @swagger.operation(**login_doc)
    def get(self):
        return {
            'status': 'healthy',
            'model_loaded': llava_analyzer.model_loaded,
            'device': llava_analyzer.device,
            'service': 'llava-image-analyzer'
        }, 200


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


class RawAnalyzeAi(Resource):
    @swagger.operation(**login_doc)
    def post(self):
        try:
            if 'image' not in request.files:
                return {"success": False, "message": "Aucun fichier fourni"}, 400

            file = request.files['image']
            if file.filename == '':
                return {"success": False, "message": "Aucun fichier sélectionné"}, 400

            # Vérifier l'extension du fichier
            if not allowed_file(file.filename):
                return {
                    'success': False,
                    'error': 'Invalid file type',
                    'message': f'Types autorisés: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}',
                    'allowed_extensions': list(current_app.config['ALLOWED_EXTENSIONS'])
                }, 400

                # Récupérer les paramètres
            prompt = request.form.get(
                'prompt', "Décris cette image en détail. Qu'est-ce que tu vois?")
            max_tokens = int(request.form.get('max_tokens', 200))
            temperature = float(request.form.get('temperature', 0.7))

            # Lire les données de l'image
            image_data = file.read()

            # Traitement de l'image
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(
            #     current_app.config['UPLOAD_FOLDER'], filename))

            # Valider que c'est une image valide
            try:
                Image.open(io.BytesIO(image_data)).verify()
            except Exception as e:
                return {
                    'success': False,
                    'error': 'Invalid image file',
                    'message': 'Le fichier fourni n\'est pas une image valide'
                }, 400

            logger.info("Image uploadée et validée avec succès")

            # Analyser l'image
            result = llava_analyzer.analyze_image(
                image_data=image_data,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return {
                'success': True,
                'analysis': result,
                'prompt_used': prompt,
                'parameters': {
                    'max_tokens': max_tokens,
                    'temperature': temperature
                }
            }, 200

        except Exception as e:
            logger.error(f"Erreur dans /api/analyze: {str(e)}")
            return {
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }, 500


class RemoteAnalyzeAi(Resource):
    @swagger.operation(**login_doc)
    def post(self):
        """
        Endpoint pour analyser une image à partir d'une URL
        Accepte: POST avec JSON contenant 'image_url' et 'prompt'
        """
        try:
            import requests

            data = request.get_json()

            if not data or 'image_url' not in data:
                return {
                    'success': False,
                    'error': 'Missing image_url',
                    'message': 'Le champ "image_url" est requis dans le corps JSON'
                }, 400

            image_url = data['image_url']
            prompt = data.get(
                'prompt',
                """Analyse cette image d'une pièce et fournis une réponse structurée en JSON en français.
    Pour chaque élément visible, indique:
    - élément: le type d'élément (mur, sol, plafond, fenêtre, porte, meuble, équipement)
    - couleur: la couleur principale
    - état: excellent, bon, moyen, mauvais, très mauvais
    - matériau: si identifiable
    - remarques: observations supplémentaires

    Réponds UNIQUEMENT avec du JSON valide sans texte supplémentaire. Format:
    {
        "analyse_globale": "description générale",
        "elements": [
            {
                "element": "type",
                "couleur": "couleur",
                "etat": "état",
                "materiau": "matériau",
                "remarques": "observations"
            }
        ],
        "resume": {
            "nombre_elements": 0,
            "etat_moyen": "moyen"
        }
    }""")
            max_tokens = data.get('max_tokens', 200)
            temperature = data.get('temperature', 0.7)

            # Télécharger l'image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            # Vérifier le type de contenu
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return {
                    'success': False,
                    'error': 'Invalid content type',
                    'message': 'L\'URL ne pointe pas vers une image valide'
                }, 400

            image_data = response.content

            # Analyser l'image
            result = llava_analyzer.analyze_image(
                image_data=image_data,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return {
                'success': True,
                'analysis': result,
                'prompt_used': prompt,
                'image_url': image_url,
                'parameters': {
                    'max_tokens': max_tokens,
                    'temperature': temperature
                }
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': 'Download failed',
                'message': f'Erreur lors du téléchargement de l\'image: {str(e)}'
            }, 400

        except Exception as e:
            logger.error(f"Erreur dans /api/analyze/url: {str(e)}")
            return {
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            }, 500
