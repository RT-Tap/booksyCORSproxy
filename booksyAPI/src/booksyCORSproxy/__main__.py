import os
from booksyCORSproxy import app, logger
import gunicorn.app.base

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)
    def load(self):
        return self.application
options = {
    'bind': f"{os.getenv('SERVERCONFIG_BINDADDR', '0.0.0.0')}:{ os.getenv('SERVERCONFIG_PORT','5000')}",
    'workers': f"{os.getenv('SERVERCONFIG_WORKERS', '20')}",
    'errorlog': f"{os.getenv('SERVERCONFIG_ERRORLOG','-')}",
    'loglevel': f"{os.getenv('LOGLVL','warning').lower()}",
    'accesslog': f"{os.getenv('SERVERCONFIG_ACCESSLOG','-')}",
}
if not os.getenv("TLS", "false").lower() == "false":
    if os.getenv("TLS").lower() == "mutual": 
        options["cert-reqs"] =  'ssl.CERT_REQUIRED'
        options["ca-certs"] = f"{os.getenv('ROOTCA_CERT', '/run/secrets/root.crt')}"
    else: 
        options["cert-reqs"] = 'ssl.CERT_NONE'
    options["certfile"] = f"{os.getenv('TLS_CERT', '/run/secrets/site.crt')}"
    options["keyfile"] = f"{os.getenv('TLS_KEY', '/run/secrets/site.key')}"
logger.info("Config:")
for key, value  in options.items(): 
    logger.info(f"{key} : {value}")
StandaloneApplication(app=app, options=options).run()
