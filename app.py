from flask import Flask, render_template, request, session, redirect, url_for, g
from pymongo import MongoClient
import os
import secrets
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

# Production-ready secret key - uses env var or generates a secure one
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Session configuration for production
app.permanent_session_lifetime = timedelta(hours=24)
app.config.update(
    SESSION_COOKIE_SECURE=os.getenv("FLASK_ENV") == "production",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)
)

# MongoDB connection with error handling
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/stockflow")
MAX_RETRIES = 3

def get_db():
    """Get database connection with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.server_info()  # Test connection
            return client["stockflow"]
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            continue
    return None

db = get_db()

@app.before_request
def inject_db():
    """Make db available to all routes."""
    g.db = db

@app.context_processor
def inject_user():
    """Make current_user available to all templates."""
    from models.user import User
    user = None
    if 'user_id' in session:
        try:
            user = User.get_by_id(db, session['user_id'])
        except Exception:
            pass  # User not found or DB error
    return dict(current_user=user)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'stockflow'}, 200

# Register Blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.dashboard import dashboard_bp
from routes.settings import settings_bp
from routes.analytics import analytics_bp
from routes.activity import activity_bp

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(activity_bp)

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug_mode, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
