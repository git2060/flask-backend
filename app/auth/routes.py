from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db, bcrypt
from ..models import User

## Authentication check to protect sensitive endpoints

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
@jwt_required()
def test():
    print(12)
    return {
        "identity": get_jwt_identity(),
        "identity_type": str(type(get_jwt_identity()))
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200
