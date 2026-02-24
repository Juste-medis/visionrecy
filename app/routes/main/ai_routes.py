

from flask import Flask, request, jsonify
from llava_processor import llava_analyzer
from PIL import Image
import io
import logging
from dotenv import load_dotenv
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': llava_analyzer.model_loaded,
        'device': llava_analyzer.device,
        'service': 'llava-image-analyzer'
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """
    Endpoint principal pour l'analyse d'image
    Accepte: POST avec form-data contenant 'image' et optionnellement 'prompt'
    """
    try:
        # Vérifier si un fichier est présent
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image provided',
                'message': 'Le champ "image" est requis'
            }), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected',
                'message': 'Aucun fichier sélectionné'
            }), 400

        # Vérifier l'extension du fichier
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type',
                'message': f'Types autorisés: {", ".join(app.config["ALLOWED_EXTENSIONS"])}',
                'allowed_extensions': list(app.config['ALLOWED_EXTENSIONS'])
            }), 400

        # Récupérer les paramètres
        prompt = request.form.get(
            'prompt', "Décris cette image en détail. Qu'est-ce que tu vois?")
        max_tokens = int(request.form.get('max_tokens', 200))
        temperature = float(request.form.get('temperature', 0.7))

        # Lire les données de l'image
        image_data = file.read()

        # Valider que c'est une image valide
        try:
            Image.open(io.BytesIO(image_data)).verify()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Invalid image file',
                'message': 'Le fichier fourni n\'est pas une image valide'
            }), 400

        # Analyser l'image
        result = llava_analyzer.analyze_image(
            image_data=image_data,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return jsonify({
            'success': True,
            'analysis': result,
            'prompt_used': prompt,
            'parameters': {
                'max_tokens': max_tokens,
                'temperature': temperature
            }
        })

    except Exception as e:
        logger.error(f"Erreur dans /api/analyze: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/analyze/url', methods=['POST'])
def analyze_image_from_url():
    """
    Endpoint pour analyser une image à partir d'une URL
    Accepte: POST avec JSON contenant 'image_url' et 'prompt'
    """
    try:
        import requests

        data = request.get_json()

        if not data or 'image_url' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing image_url',
                'message': 'Le champ "image_url" est requis dans le corps JSON'
            }), 400

        image_url = data['image_url']
        prompt = data.get(
            'prompt', "Décris cette image en détail. Qu'est-ce que tu vois?")
        max_tokens = data.get('max_tokens', 200)
        temperature = data.get('temperature', 0.7)

        # Télécharger l'image
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        # Vérifier le type de contenu
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return jsonify({
                'success': False,
                'error': 'Invalid content type',
                'message': 'L\'URL ne pointe pas vers une image valide'
            }), 400

        image_data = response.content

        # Analyser l'image
        result = llava_analyzer.analyze_image(
            image_data=image_data,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return jsonify({
            'success': True,
            'analysis': result,
            'prompt_used': prompt,
            'image_url': image_url,
            'parameters': {
                'max_tokens': max_tokens,
                'temperature': temperature
            }
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': 'Download failed',
            'message': f'Erreur lors du téléchargement de l\'image: {str(e)}'
        }), 400
    except Exception as e:
        logger.error(f"Erreur dans /api/analyze/url: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'success': False,
        'error': 'File too large',
        'message': 'Le fichier est trop volumineux (max 16MB)'
    }), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'Endpoint non trouvé'
    }), 404
