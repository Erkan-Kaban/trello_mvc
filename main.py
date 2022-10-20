from flask import Flask
from controllers.cards_controller import cards_bp
from db import db, ma
import os


# db = SQLAlchemy()
# ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config ['JSON_SORT_KEYS'] = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(cards_bp)

    return app