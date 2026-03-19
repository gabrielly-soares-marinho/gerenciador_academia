from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, static_folder="../frontend", static_url_path="/")

    # allow test override config first
    if test_config:
        app.config.update(test_config)

    # default configuration
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URI')
    if not db_uri:
        raise RuntimeError(
            "DATABASE_URI is required and must point to MySQL, e.g. mysql+pymysql://root:password@db:3306/academia"
        )

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    migrate.init_app(app, db)

    # import models so they are registered with SQLAlchemy
    from . import models
    from .views import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception('Unexpected server error')
        return jsonify({'error': 'Internal server error', 'detail': str(error)}), 500

    return app
