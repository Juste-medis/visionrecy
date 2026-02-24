from schema import Schema, And, Use, Optional, SchemaError, Or
from datetime import datetime


def validate_data(data, schema):
    try:
        return schema.validate(data), None
    except SchemaError as e:
        return False, str(e)


# Schema for School model
def getschool_schema(t):
    thedic = {
        'name': And(str, len, error="Le nom de l'école est requis et doit être une chaîne non vide."),
        'address': And(str, len, error="L'adresse doit être une chaîne non vide."),
        Optional('contact_email'): And(str, lambda s: '@' in s, error="L'adresse e-mail de contact doit être valide."),
    }

    if t == "u":  # Mode "update"
        return Schema({
            Optional('name'): Or(str, None),
            Optional('address'): Or(str, None),
            Optional('contact_email'): Or(str, None),
        })

    return Schema(thedic)


def get_module_schema(t):
    thedict = {
        'school_id': And(int, error="L'école associée est requise."),
        'title': And(str, len, error="Le titre est requis."),
        Optional('description', default=""): str,
        Optional('module_type', default="General"): str
    }

    if t == "u":  # Mode "update"
        thedict = {
            Optional('school_id'): And(int, error="L'école associée est requise."),
            Optional('title'): And(str, len, error="Le titre est requis."),
            Optional('description', default=""): str,
            Optional('module_type', default="General"): str
        }

    return Schema(thedict)


def get_challenge_shema(is_update=False):
    return Schema({
        Optional('title', default=None) if is_update else 'title': And(str, len, lambda s: 3 <= len(s) <= 100),
        Optional('description', default=None) if is_update else 'description': And(str, len, lambda s: len(s) <= 500),
        Optional('reward_points', default=None) if is_update else 'reward_points': And(Use(int), lambda n: n >= 0),
        Optional('goal', default=None) if is_update else 'goal': And(Use(int), lambda n: n >= 0),
        Optional('start_date', default=None) if is_update else 'start_date': And(str, Use(lambda s: datetime.fromisoformat(s))),
        Optional('expiration_date', default=None) if is_update else 'expiration_date': And(str, Use(lambda s: datetime.fromisoformat(s))),
    })


def get_userchallenge_shema(is_update=False):
    return Schema({
        Optional('challenge_id', default=None) if is_update else 'challenge_id': And(Use(int), lambda n: n >= 0),
        Optional('user_id', default=None) if is_update else 'user_id': And(Use(int), lambda n: n >= 0),
        Optional('progress', default=None) if is_update else 'progress': And(Use(int), lambda n: n >= 0),
        Optional('completed_at', default=None) if is_update else 'completed_at': And(str, Use(lambda s: datetime.fromisoformat(s))),
    })


# Schema for EducationalModule model
educational_module_schema = Schema({
    'school_id': And(int, lambda n: n > 0, error="L'ID de l'école doit être un entier positif."),
    'title': And(str, len, error="Le titre du module est requis et doit être une chaîne non vide."),
    Optional('module_type'): str,
    Optional('description'): str,
})

# Schema for UserModule model
user_module_schema = Schema({
    'user_id': And(int, lambda n: n > 0, error="L'ID de l'utilisateur doit être un entier positif."),
    'module_id': And(int, lambda n: n > 0, error="L'ID du module doit être un entier positif."),
    Optional('score'): And(Use(float), lambda n: 0 <= n <= 100, error="Le score doit être un nombre entre 0 et 100."),
    Optional('completed_at'): And(str, Use(lambda x: datetime.fromisoformat(x)), error="La date de complétion doit être au format ISO.")
})

# Schema for RecyclingEvent model
recycling_event_schema = Schema({
    'title': And(str, len, error="Le titre de l'événement est requis et doit être une chaîne non vide."),
    'description': str,
    'location': And(str, error="L'addresse de l'évènement est recquise"),
    'event_date': And(str, Use(lambda x: datetime.fromisoformat(x)), error="La date de l'événement doit être au format ISO."),
})

# Schema for EventNotification model
event_notification_schema = Schema({
    'user_id': And(int, lambda n: n > 0),
    'event_id': And(int, lambda n: n > 0),
    Optional('sent_at'): And(str, Use(lambda x: datetime.fromisoformat(x)))
})
