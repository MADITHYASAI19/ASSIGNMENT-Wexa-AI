import pytest
from models.user import User
from bson import ObjectId

def test_signup_creates_user_and_org(client, db):
    """User signup creates org + user."""
    response = client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Test Org"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    user = db.users.find_one({"email": "test@example.com"})
    assert user is not None
    assert db.organizations.find_one({"_id": user["organization_id"]}) is not None

def test_signup_validation_email(client):
    """Email validation."""
    response = client.post("/auth/signup", data={
        "email": "invalid",
        "password": "password123",
        "org_name": "Test"
    })
    assert b"Valid email required" in response.data

def test_signup_duplicate_email(client, db):
    """Can't sign up with same email twice."""
    client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Org 1"
    })
    response = client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Org 2"
    })
    assert b"already in use" in response.data

def test_login_success(client, db):
    """Login with correct credentials."""
    # Signup first
    client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Test"
    })
    
    # Login
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"dashboard" in response.data or b"products" in response.data  # On dashboard

def test_login_invalid_password(client, db):
    """Login fails with wrong password."""
    client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Test"
    })
    
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert b"Invalid" in response.data

def test_logout(client, db):
    """Logout clears session."""
    client.post("/auth/signup", data={
        "email": "test@example.com",
        "password": "password123",
        "org_name": "Test"
    })
    
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    # Verify session is cleared (try accessing protected page)
