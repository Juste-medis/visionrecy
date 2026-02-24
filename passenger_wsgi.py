import sys
import os
import json
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

logfile = open('logs/app.log', 'a')
sys.stdout = logfile
sys.stderr = logfile

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
application = create_app() 
print("🚀 Application démarrée avec Passenger")
