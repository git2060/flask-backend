from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
bcrypt = Bcrypt()
jwt = JWTManager()