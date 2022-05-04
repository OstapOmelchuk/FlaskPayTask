import os

from flask import Flask
from dotenv import load_dotenv

from db.database import db
from product_payment_api.views import payment_view

load_dotenv()

template_dir = os.path.abspath('product_payment_api/template')


def create_app():
    app = Flask(__name__, template_folder=template_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv("SECRET_KEY")

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)


def setup_database(app):
    with app.app_context():
        db.create_all()


def register_blueprints(app):
    app.register_blueprint(payment_view.blp)
    return None


if __name__ == '__main__':
    app = create_app()
    setup_database(app)
    app.run(debug=True)
