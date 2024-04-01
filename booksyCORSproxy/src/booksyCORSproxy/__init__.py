from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import sys
import logging

logger = logging.getLogger()
lvl = logging.INFO if os.getenv("LOGLVL") is None else logging.getLevelName(os.getenv("LOGLVL").upper())
logger.setLevel(lvl)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S'))
logger.addHandler(stdout_handler)

app = Flask(__name__)
if os.getenv("MODE", "production").lower() != "production":
    CORS(app, resources={r"*": {"origins": "*"}})
    logger.info("---Setup for development ---")
else:
    if os.getenv("BOOKSYAPI_PROXY", "false").lower() == "true": 
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) # letting flask know its beghind a proxy
    # config refrence: https://flask.palletsprojects.com/en/2.1.x/config/
    app.config.update(      
        ENV='production',
        TESTING=False,
        # to get your own run secure secret: python -c 'import secrets; print(secrets.token_hex())'
        SECRET_KEY=os.getenv("SECRET_KEY", "DEFAULT-CHANGEME"),  
        APPLICATION_ROOT=os.getenv("ROOT_PATH", '/boorev_api'),
    )
    if os.getenv("SERVER_NAME"): 
        app.config.update( SERVER_NAME=os.getenv("SERVER_NAME"))
    CORS(app, resources={r"*": {"origins": os.getenv("SERVER_NAME", "*")}})
    logger.info("---Setup for production ---")
import booksyCORSproxy.views

