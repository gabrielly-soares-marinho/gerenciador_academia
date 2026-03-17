from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, static_folder="../frontend", static_url_path="/")

    # default configuration
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI', 'mysql+pymysql://root:password@db:3306/academia'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # allow test or override config
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # import models so they are registered with SQLAlchemy
    from . import models
    from .views import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app
