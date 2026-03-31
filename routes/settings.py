from flask import Blueprint, render_template, request, session, g, redirect, url_for
from models.organization import Organization

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")

@settings_bp.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    org_id = session["organization_id"]
    
    if request.method == "POST":
        threshold = request.form.get("global_threshold", 5)
        try:
            threshold = int(threshold)
            Organization.set_low_stock_threshold(g.db, org_id, threshold)
            from flask import flash
            flash("Settings saved successfully!", "success")
        except:
            pass
        return redirect(url_for("settings.index"))
        
    org = Organization.get_by_id(g.db, org_id)
    threshold = org.get("default_low_stock_threshold", 5) if org else 5
    
    return render_template("settings.html", threshold=threshold, organization_id=org_id)
