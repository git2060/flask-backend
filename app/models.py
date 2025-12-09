from datetime import datetime
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    budgets = db.relationship("Budget", backref="user", lazy=True)

class Budget(db.Model):
    """
    Stores the latest budget for a given user + month.
    For simplicity we'll assume a single active budget per user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Store BudgetBox fields
    income = db.Column(db.Float, nullable=False, default=0)
    monthly_bills = db.Column(db.Float, nullable=False, default=0)
    food = db.Column(db.Float, nullable=False, default=0)
    transport = db.Column(db.Float, nullable=False, default=0)
    subscriptions = db.Column(db.Float, nullable=False, default=0)
    miscellaneous = db.Column(db.Float, nullable=False, default=0)

    # Keep full JSON also, for flexibility
    raw_json = db.Column(db.JSON, nullable=False)

    # Sync info
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_synced_at = db.Column(db.DateTime, nullable=True)
