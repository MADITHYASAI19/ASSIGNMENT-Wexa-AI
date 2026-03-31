import pytest
from app import app as flask_app
from pymongo import MongoClient
from models.user import User
from bson import ObjectId

@pytest.fixture
def app():
    """Flask app for testing."""
    flask_app.config["TESTING"] = True
    return flask_app

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def db(app):
    """MongoDB connection (test DB)."""
    client = MongoClient("mongodb://localhost:27017/stockflow_test")
    database = client["stockflow_test"]
    
    # Create indexes
    database.users.create_index("email", unique=True)
    
    yield database
    
    # Cleanup
    client.drop_database("stockflow_test")

@pytest.fixture
def auth_user(client, db):
    """Authenticated user with org."""
    response = client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Test Org"
    })
    
    user = db.users.find_one({"email": "test@example.com"})
    return {
        "_id": str(user["_id"]),
        "organization_id": str(user["organization_id"])
    }
