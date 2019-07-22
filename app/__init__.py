import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from config import Config


#db object represents the database
db = SQLAlchemy()
#migrate object represents the migration engine
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
#flask mail instance
mail = Mail()
#flask bootstrap instance
bootstrap = Bootstrap()
#flask moment instance to get moment.js for timestamp
moment = Moment()
#flask babel instance to get translations of languages
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    boostrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    #using conditional expression to make Elasticsearch instance None
    #when a URL for the service wasn't defined in Environment
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    #register the errors blueprint with the application
    from app.errors import bp as errors_bp
    #using register_blueprint method is used -- so that anything used
    #within the application is connected
    app.register_blueprint(errors_bp)

    #register the authentication blueprint with the application
    from app.auth import bp as auth_bp
    #calls url_prefix -- to attachh blueprint under URL prefixx
    #routes defined in blueprint get this prefix in URLs
    app.register_blueprint(auth_bp, url_prefix = '/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)



    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
            #writing the log file with name microblog.log in a logs
            #directory -- created if not already exists
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        #rotatingfilehandler rotates the log ensuring the log files
        #do not grow too large -- limit the size of the file
        #keeping the last ten log files as backup

        #formatter provides custom formatting to the messages
        #include timestamp, the logging level, message and source file -- plus line #
        #where the log entry originated
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        #logging level categories: debug, info, warning, error, and critical in increasing
        #order of severity
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

#using request object called accept_languages -- this works with accept
#language header when clients send a request
@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'es'

#new_version -- remove errors from import 
from app import models
#importing models which will define the structure of the
#database

#init.py are used to mark directories on a disk as python packate directories. 
#python looks for the submodules to import them in this file
