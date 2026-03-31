from flask import Blueprint, render_template, session, redirect, url_for, g
from functools import wraps
from datetime import datetime, timedelta
from bson import ObjectId

activity_bp = Blueprint("activity", __name__, url_prefix="/activity")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@activity_bp.route("/")
@login_required
def index():
    org_id = session["organization_id"]
    
    # Fetch real activity from database or generate from products
    db_activities = list(g.db.activity_log.find({"organization_id": ObjectId(org_id)}).sort("timestamp", -1).limit(20))
    
    activities = []
    now = datetime.utcnow()
    
    if db_activities:
        for act in db_activities:
            activities.append({
                "_id": str(act.get("_id", "")),
                "action": act.get("action", "update"),
                "user_email": act.get("user_email", "system@stockflow.ai"),
                "product_name": act.get("product_name", "Unknown"),
                "product_id": str(act.get("product_id", "")),
                "timestamp": act.get("timestamp", now)
            })
    else:
        # Generate mock activities with proper datetime objects
        mock_data = [
            ("update", "Arc Reactor Mk4 adjusted: 12 → 10", timedelta(hours=2)),
            ("create", "Nano-Particle Canister created", timedelta(hours=5)),
            ("delete", "Unibeam Emitter removed", timedelta(days=1)),
            ("update", "Vibranium Alloy stock updated", timedelta(days=2)),
        ]
        
        for action, message, time_delta in mock_data:
            ts = now - time_delta
            activities.append({
                "_id": f"mock_{action}_{time_delta}",
                "action": action,
                "user_email": "tony@stark.com",
                "product_name": message.replace(" adjusted", "").replace(" created", "").replace(" removed", "").replace(" stock updated", ""),
                "product_id": "mock-product-id",
                "timestamp": ts
            })
    
    return render_template("activity/log.html", activities=activities)
