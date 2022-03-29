'''
Tokenizer service. To run the service in production:
waitress-serve --port=5000 --call 'application:create_app'

Created on July 7, 2020

@author: Shuai Liang
'''

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask.logging import default_handler

import logging
import logging.handlers
from time import strftime

from config import Config 

db = SQLAlchemy()
def create_app(**custom_conf):
    app = Flask(__name__)
    # load and update config
    app.config.from_object(Config)
    app.config.update(custom_conf)

    db = SQLAlchemy(app)
    
    from token_gen.models import Token
    db.create_all()
    db.session.commit()

    app.logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        app.config['LOGNAME'], maxBytes=app.config['MBYTES'], backupCount=app.config['NFILES'])
    formatter = logging.Formatter("%(asctime)s-%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    app.url_map.strict_slashes = False

    #import blueprints
    from home.views import home_app
    from token_gen.views import token_app
    #register blueprints
    app.register_blueprint(home_app)
    app.register_blueprint(token_app)

    @app.errorhandler(500)
    def internal_error(exception):
        app.logger.error(exception)
        return 'internal error', 500
    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        # This avoids the duplication of registry in the log,
        # since that 500 is already logged via @app.errorhandler.
        if response.status_code != 500:
            app.logger.info('%s %s %s %s %s',
                        request.remote_addr,
                        request.method,
                        request.scheme,
                        request.full_path,
                        response.status)
        return response
    return app
