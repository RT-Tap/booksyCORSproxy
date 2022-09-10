from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
if os.getenv("FLASK_DEBUG") == True: stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S'))
logger.addHandler(stdout_handler)
app = Flask(__name__)
if os.getenv("FLASK_DEBUG", True) == "False":
    if os.getenv("BOOKSYAPI_PROXY", False) == True: app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) # letting flask know its beghind a proxy
    # config refrence: https://flask.palletsprojects.com/en/2.1.x/config/
    app.config.update(      
        ENV='production',
        TESTING=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "DEFAULT-CHANGEME"),  # to get your own run: python -c 'import secrets; print(secrets.token_hex())'
        APPLICATION_ROOT='/api',
    )
    if os.getenv("SERVER_NAME"): app.config.update( SERVER_NAME=os.getenv("SERVER_NAME"))
    CORS(app, resources={r"*": {"origins": os.getenv("SERVER_NAME")}})
    logger.info("Starting app in production mode")
else:
    CORS(app, resources={r"*": {"origins": "*"}})
    logger.info("Starting app in development mode")
import booksyAPI.views

