from flask import Blueprint, render_template, request, session, g, redirect, url_for
from models.organization import Organization

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    org_id = session["organization_id"]
    org = Organization.get_by_id(g.db, org_id)
    threshold = org.get("default_low_stock_threshold", 5) if org else 5
    
    return render_template("settings.html", threshold=threshold)

@settings_bp.route("/set-threshold", methods=["POST"])
def set_threshold():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    org_id = session["organization_id"]
    threshold = request.form.get("threshold", 5)
    
    try:
        threshold = int(threshold)
        Organization.set_low_stock_threshold(g.db, org_id, threshold)
    except:
        pass
    
    return redirect(url_for("settings.index"))
