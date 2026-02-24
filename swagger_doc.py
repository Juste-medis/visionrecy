# swagger_doc.py

login_doc = {
    "notes": "Connecte un utilisateur avec email et mot de passe",
    "nickname": "login",
    "parameters": [
        {
            "name": "body",
            "description": "Données de connexion",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "email": "string",
                "password": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Connexion réussie"},
        {"code": 400, "message": "Erreur de connexion"},
    ]
}

register_doc = {
    "notes": "Inscrit un nouvel utilisateur",
    "nickname": "register",
    "parameters": [
        {
            "name": "body",
            "description": "Données d'inscription",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "username": "string",
                "email": "string",
                "password": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 201, "message": "Inscription réussie"},
        {"code": 400, "message": "Erreur lors de l'inscription"},
    ]
}

logout_doc = {
    "notes": "Déconnecte l'utilisateur (simulé, pas de suppression de token côté serveur)",
    "nickname": "logout",
    "responseMessages": [
        {"code": 200, "message": "Déconnexion réussieddddd"},
    ]
}

# --------------------main route-------------------------------------------------------
upload_doc = {
    "notes": "Permet à l'utilisateur de télécharger un fichier image pour analyse",
    "nickname": "upload",
    "parameters": [
        {
            "name": "Authorization",
            "description": "Token d'authentification JWT. Format: Bearer <token>",
            "required": True,
            "allowMultiple": False,
            "dataType": "string",
            "paramType": "header"
        },
        {
            "name": "file",
            "description": "Le fichier image à traiter",
            "required": True,
            "allowMultiple": False,
            "dataType": "file",
            "paramType": "form"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Classification réussie"},
        {"code": 400, "message": "Erreur lors du téléchargement ou traitement du fichier"}
    ]
}

history_doc = {
    "notes": "Récupère l'historique des prédictions pour l'utilisateur connecté",
    "nickname": "history",
    "responseMessages": [
        {"code": 200, "message": "Historique récupéré avec succès"},
        {"code": 401, "message": "Utilisateur non authentifié"}
    ]
}
# Documentation pour les Écoles

# Créer une nouvelle école
create_school_doc = {
    "notes": "Créer une nouvelle école",
    "nickname": "create",
    "parameters": [
        {
            "name": "body",
            "description": "Données de l'école à créer",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "id": "School",
                "name": "string",
                "location": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 201, "message": "École créée avec succès"},
        {"code": 400, "message": "Erreur de création de l'école"}
    ]
}

# Récupérer la liste de toutes les écoles
get_schools_doc = {
    "nickname": "get",
    "notes": "Récupérer la liste de toutes les écoles",
    "responseMessages": [
        {"code": 200, "message": "Liste des écoles récupérée avec succès"},
        {"code": 500, "message": "Erreur lors de la récupération des écoles"}
    ]
}

# Récupérer les détails d’une école
get_school_doc = {
    "nickname": "getunity",
    "notes": "Récupérer les détails d’une école",
    "parameters": [
        {
            "name": "school_id",
            "description": "ID de l'école",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Détails de l'école récupérés avec succès"},
        {"code": 404, "message": "École non trouvée"}
    ]
}

# Mettre à jour les informations d’une école
update_school_doc = {
    "nickname": "update",
    "notes": "Mettre à jour les informations d’une école",
    "parameters": [
        {
            "name": "school_id",
            "description": "ID de l'école à mettre à jour",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        },
        {
            "name": "body",
            "description": "Nouvelles informations de l'école",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "name": "string",
                "location": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "École mise à jour avec succès"},
        {"code": 400, "message": "Erreur lors de la mise à jour de l'école"}
    ]
}

# Supprimer une école
delete_school_doc = {
    "nickname": "delete_school_doc",
    "notes": "Supprimer une école",
    "parameters": [
        {
            "name": "school_id",
            "description": "ID de l'école à supprimer",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "École supprimée avec succès"},
        {"code": 404, "message": "École non trouvée"}
    ]
}

# Documentation pour les Challenges

# Créer un nouveau challenge
create_challenge_doc = {
    "nickname": "create_challenge_doc",
    "notes": "Créer un nouveau challenge",
    "parameters": [
        {
            "name": "body",
            "description": "Données du challenge à créer",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "id": "Challenge",
                "title": "string",
                "description": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 201, "message": "Challenge créé avec succès"},
        {"code": 400, "message": "Erreur de création du challenge"}
    ]
}

create_cuserhallenge_doc = {
    "nickname": "create_cuserhallenge_doc",
    "notes": "Pour inscrire un utilisateur à un challenge",
    "parameters": [
        {
            "name": "body",
            "description": "Données de l'inscription à créer",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "id": "UserChallenge",
                "title": "string",
                "description": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 201, "message": "Incription éffectuée créé avec succès"},
        {"code": 400, "message": "Erreur lors de l'inscription"}
    ]
}

# Récupérer tous les challenges
get_challenges_doc = {
    "nickname": "get_challenges_doc",
    "notes": "Récupérer tous les challenges",
    "responseMessages": [
        {"code": 200, "message": "Liste des challenges récupérée avec succès"},
        {"code": 500, "message": "Erreur lors de la récupération des challenges"}
    ]
}

# Récupérer un challenge spécifique
get_challenge_doc = {
    "nickname": "get_challenge_doc",
    "notes": "Récupérer un challenge spécifique",
    "parameters": [
        {
            "name": "challenge_id",
            "description": "ID du challenge",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Détails du challenge récupérés avec succès"},
        {"code": 404, "message": "Challenge non trouvé"}
    ]
}

# Mettre à jour un challenge
update_challenge_doc = {
    "nickname": "update_challenge_doc",
    "notes": "Mettre à jour un challenge",
    "parameters": [
        {
            "name": "challenge_id",
            "description": "ID du challenge à mettre à jour",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        },
        {
            "name": "body",
            "description": "Nouvelles informations du challenge",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "title": "string",
                "description": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Challenge mis à jour avec succès"},
        {"code": 400, "message": "Erreur lors de la mise à jour du challenge"}
    ]
}

# Supprimer un challenge
delete_challenge_doc = {
    "nickname": "delete_challenge_doc",
    "notes": "Supprimer un challenge",
    "parameters": [
        {
            "name": "challenge_id",
            "description": "ID du challenge à supprimer",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Challenge supprimé avec succès"},
        {"code": 404, "message": "Challenge non trouvé"}
    ]
}
# Créer un module éducatif
create_module = {
    "notes": "Créer un nouveau module éducatif",
    "nickname": "create_module",
    "parameters": [
        {
            "name": "body",
            "description": "Données du module à créer",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "school_id": "integer",
                "title": "string",
                "description": "string",
                "module_type": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 201, "message": "Module créé avec succès"},
        {"code": 400, "message": "Erreur de création du module"}
    ]
}

# Récupérer la liste de tous les modules
get_modules = {
    "nickname": "get_modules",
    "notes": "Récupérer la liste de tous les modules éducatifs",
    "responseMessages": [
        {"code": 200, "message": "Liste des modules récupérée avec succès"},
        {"code": 500, "message": "Erreur lors de la récupération des modules"}
    ]
}

# Récupérer les détails d’un module
get_module = {
    "nickname": "get_module",
    "notes": "Récupérer les détails d’un module éducatif",
    "parameters": [
        {
            "name": "module_id",
            "description": "ID du module",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Détails du module récupérés avec succès"},
        {"code": 404, "message": "Module non trouvé"}
    ]
}

# Mettre à jour un module éducatif
modify_module = {
    "nickname": "modify_module",
    "notes": "Mettre à jour les informations d’un module éducatif",
    "parameters": [
        {
            "name": "module_id",
            "description": "ID du module à mettre à jour",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        },
        {
            "name": "body",
            "description": "Nouvelles informations du module",
            "required": True,
            "allowMultiple": False,
            "dataType": "object",
            "paramType": "body",
            "schema": {
                "title": "string",
                "description": "string",
                "module_type": "string"
            }
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Module mis à jour avec succès"},
        {"code": 400, "message": "Erreur lors de la mise à jour du module"}
    ]
}

# Supprimer un module éducatif
delete_module = {
    "nickname": "delete_module",
    "notes": "Supprimer un module éducatif",
    "parameters": [
        {
            "name": "module_id",
            "description": "ID du module à supprimer",
            "required": True,
            "dataType": "integer",
            "paramType": "path"
        }
    ],
    "responseMessages": [
        {"code": 200, "message": "Module supprimé avec succès"},
        {"code": 404, "message": "Module non trouvé"}
    ]
}
password_reset_request_doc = {
    'parameters': [
        {
            'name': 'email',
            'description': 'User email',
            'required': True,
            'dataType': 'string',
            'paramType': 'body'
        }
    ],
    'responseMessages': [
        {'code': 200, 'message': 'Reset link sent'},
        {'code': 400, 'message': 'Invalid email'}
    ]
}

password_reset_confirm_doc = {
    'parameters': [
        {
            'name': 'token',
            'description': 'Password reset token',
            'required': True,
            'dataType': 'string',
            'paramType': 'body'
        },
        {
            'name': 'new_password',
            'description': 'New password',
            'required': True,
            'dataType': 'string',
            'paramType': 'body'
        }
    ],
    'responseMessages': [
        {'code': 200, 'message': 'Password reset successful'},
        {'code': 400, 'message': 'Invalid token or password'}
    ]
}

password_change_doc = {
    'parameters': [
        {
            'name': 'current_password',
            'description': 'Current password',
            'required': True,
            'dataType': 'string',
            'paramType': 'body'
        },
        {
            'name': 'new_password',
            'description': 'New password',
            'required': True,
            'dataType': 'string',
            'paramType': 'body'
        }
    ],
    'responseMessages': [
        {'code': 200, 'message': 'Password changed successfully'},
        {'code': 400, 'message': 'Invalid current password or new password'},
        {'code': 401, 'message': 'Unauthorized'}
    ]
}