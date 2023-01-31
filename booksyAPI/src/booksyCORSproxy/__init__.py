from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
if os.getenv("FLASK_DEBUG").lower() == "true": stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S'))
logger.addHandler(stdout_handler)
# we configure gunicorn 
interface = f"--bind={os.getenv('SERVERCONFIG_BINDADDR', '0.0.0.0')}:{ os.getenv('SERVERCONFIG_PORT','5000')}"
workerthreads = f"--workers={os.getenv('SERVERCONFIG_WORKERS', '20')}"
logfile = f"--access-logfile {os.getenv('SERVERCONFIG_ACCESSLOG','-')}" #https://docs.gunicorn.org/en/20.1.0/settings.html#syslog
# refrence: https://docs.python.org/3/library/ssl.html#ssl.CERT_REQUIRED 
TLSsettings = ''
if not os.getenv("TLS", "false").lower() == "false":
    if os.getenv("TLS").lower() == "mutual": 
        TLSsettings +=  f"--cert-reqs {os.getenv('', 'ssl.CERT_REQUIRED')}"
        TLSsettings +=  f"--ca-certs {os.getenv('', '/run/secrets/root.crt')}"
    else: 
        TLSsettings +=  f"--cert-reqs {os.getenv('', 'ssl.CERT_NONE')}"
    TLSsettings +=  f"--certfile {os.getenv('TLS_CERT', '/run/secrets/site.crt')}" 
    TLSsettings +=  f"--keyfile {os.getenv('TLS_KEY', '/run/secrets/site.key')}"
allowedciphers = "--ciphers ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256"
os.environ["GUNICORN_CMD_ARGS"] = f"{interface} {workerthreads} {logfile} {TLSsettings} {allowedciphers}"
app = Flask(__name__)
if os.getenv("FLASK_DEBUG", "true").lower() == "false":
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
    if os.getenv("SERVER_NAME"): app.config.update( SERVER_NAME=os.getenv("SERVER_NAME"))
    CORS(app, resources={r"*": {"origins": os.getenv("SERVER_NAME", "*")}})
    logger.info("Starting app in production mode")
else:
    CORS(app, resources={r"*": {"origins": "*"}})
    logger.info("Starting app in development mode")
import booksyCORSproxy.views

