import os
from flask import current_app
from .extensions import db, bcrypt
from .models import User

def register_cli(app):
    @app.cli.command("seed-demo-user")
    def seed_demo_user():
        email = os.getenv("DEMO_EMAIL", "hire-me@anshumat.org")
        password = os.getenv("DEMO_PASSWORD", "HireMe@2025!")
        if User.query.filter_by(email=email).first():
            print("Demo user already exists")
            return

        user = User(
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode("utf-8")
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created demo user {email}")
