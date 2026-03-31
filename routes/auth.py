from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from models.user import User
from datetime import datetime
import re

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        org_name = request.form.get("org_name", "").strip()
        
        # Validation
        errors = []
        if not email or "@" not in email:
            errors.append("Valid email required.")
        if not password or len(password) < 6:
            errors.append("Password must be 6+ characters.")
        if not org_name or len(org_name) < 2:
            errors.append("Organization name required.")
        
        if errors:
            return render_template("auth/signup.html", errors=errors), 400
        
        # Create user
        user = User.create(g.db, email, password, org_name)
        if not user:
            return render_template("auth/signup.html", errors=["Email already in use."]), 400
        
        # Log them in
        session["user_id"] = user["_id"]
        session["organization_id"] = user["organization_id"]
        return redirect(url_for("dashboard.index"))
    
    return render_template("auth/signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        user = User.verify_login(g.db, email, password)
        if not user:
            return render_template("auth/login.html", error="Invalid email or password."), 401
        
        session["user_id"] = user["_id"]
        session["organization_id"] = user["organization_id"]
        return redirect(url_for("dashboard.index"))
    
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
