# server/wsgi.py

import os
from app import create_app

app = create_app(config_name=os.environ.get('APP_SETTINGS'))
