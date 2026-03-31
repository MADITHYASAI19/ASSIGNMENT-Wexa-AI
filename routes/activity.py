from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps

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
    # Mock data for demonstration of the timeline view
    activities = [
        {
            "id": "1",
            "type": "update",
            "message": "Sarah adjusted Mega Widget qty: 50 → 45",
            "product_id": "WGT-001",
            "time_ago": "2 hours ago",
            "icon": "✏️",
            "color": "blue",
            "initials": "SA"
        },
        {
            "id": "2",
            "type": "create",
            "message": "You created a new product",
            "product_id": "PRD-992",
            "time_ago": "5 hours ago",
            "icon": "📦",
            "color": "emerald",
            "initials": "ME"
        },
        {
            "id": "3",
            "type": "delete",
            "message": "System deleted outdated item",
            "product_id": "OLD-9",
            "time_ago": "1 day ago",
            "icon": "🗑️",
            "color": "rose",
            "initials": "SY"
        },
        {
            "id": "4",
            "type": "update",
            "message": "Sarah imported 45 products via CSV",
            "product_id": "-",
            "time_ago": "2 days ago",
            "icon": "📥",
            "color": "purple",
            "initials": "SA"
        }
    ]
    return render_template("activity/log.html", activities=activities)
