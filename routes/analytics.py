from flask import Blueprint, render_template, session, g, redirect, url_for
from functools import wraps

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@analytics_bp.route("/")
@login_required
def index():
    return render_template("analytics/dashboard.html")
