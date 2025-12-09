import os
from flask import Flask
from .config import config_map
from .extensions import db, migrate, cors, bcrypt, jwt
from .cli import register_cli
from flasgger import Swagger

from dotenv import load_dotenv
load_dotenv()

def create_app():
    env = os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)

    # load config
    app.config.from_object(config_map[env])

    # JWT secret (can reuse SECRET_KEY or separate)
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    register_cli(app)
    Swagger(app)

    from .auth.routes import auth_bp
    from .budget.routes import budget_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(budget_bp, url_prefix="/budget")


    # CORS
    return app

