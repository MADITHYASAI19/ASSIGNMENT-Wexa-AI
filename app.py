from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-key-change-in-prod"  # For sessions

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/stockflow")
client = MongoClient(MONGO_URI)
db = client["stockflow"]

@app.before_request
def inject_db():
    """Make db available to all routes."""
    from flask import g
    g.db = db

# Register Blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.dashboard import dashboard_bp
from routes.settings import settings_bp

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(settings_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
