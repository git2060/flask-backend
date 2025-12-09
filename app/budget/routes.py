from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Budget
from ..schemas import BudgetSchema, BudgetResponseSchema

budget_bp = Blueprint("budget", __name__)
budget_schema = BudgetSchema()
budget_response_schema = BudgetResponseSchema()




@budget_bp.route("/sync", methods=["POST"])
@jwt_required()
def sync_budget():
    print(1)
    """
    POST /budget/sync
    Body: budget object with fields:
        income, monthly_bills, food, transport, subscriptions, miscellaneous
    Saves or updates the user's latest budget.
    Returns: { success: true, timestamp: ... , budget: ... }
    """
    user_id = get_jwt_identity()
    print(user_id)
    payload = request.get_json() or {}
    print(payload)

    # validate budget
    data = budget_schema.load(payload)

    budget = Budget.query.filter_by(user_id=user_id).first()
    now = datetime.utcnow()

    if not budget:
        budget = Budget(
            user_id=user_id,
            raw_json=payload,
            updated_at=now,
            income=data["income"],
            monthly_bills=data["monthly_bills"],
            food=data["food"],
            transport=data["transport"],
            subscriptions=data["subscriptions"],
            miscellaneous=data["miscellaneous"],
            last_synced_at=now,
        )
        db.session.add(budget)
    else:
        budget.raw_json = payload
        budget.income = data["income"]
        budget.monthly_bills = data["monthly_bills"]
        budget.food = data["food"]
        budget.transport = data["transport"]
        budget.subscriptions = data["subscriptions"]
        budget.miscellaneous = data["miscellaneous"]
        budget.updated_at = now
        budget.last_synced_at = now

    db.session.commit()

    return jsonify({
        "success": True,
        "timestamp": now.isoformat(),
        "budget": budget_response_schema.dump(budget),
    }), 200


@budget_bp.route("/latest", methods=["GET"])
@jwt_required()
def latest_budget():
    """
    GET /budget/latest
    Returns: latest budget object for the logged-in user.
    """
    user_id = get_jwt_identity()
    budget = Budget.query.filter_by(user_id=user_id).first()
    if not budget:
        return jsonify({"budget": None}), 200

    return jsonify({
        "budget": budget_response_schema.dump(budget)
    }), 200
