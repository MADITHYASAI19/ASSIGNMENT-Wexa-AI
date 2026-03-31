import pytest
from models.user import User
from bson import ObjectId

def test_no_cross_org_data_leak_products(client, db):
    """Org A can't see Org B's products."""
    # Create user A + org A
    response_a = client.post("/auth/signup", data={
        "email": "user_a@example.com",
        "password": "password123",
        "org_name": "Org A"
    })
    user_a = db.users.find_one({"email": "user_a@example.com"})
    org_a_id = user_a["organization_id"]
    
    # Login as A, create product
    client.post("/auth/login", data={
        "email": "user_a@example.com",
        "password": "password123"
    }, follow_redirects=True)
    
    client.post("/products/create", data={
        "name": "Secret Widget",
        "sku": "SECRET-001",
        "quantity": "100"
    })
    
    # Logout A
    client.get("/auth/logout")
    
    # Create user B + org B
    response_b = client.post("/auth/signup", data={
        "email": "user_b@example.com",
        "password": "password123",
        "org_name": "Org B"
    })
    
    # Login as B, check products
    response = client.get("/products/", follow_redirects=True)
    
    # User B should NOT see Org A's product
    assert b"Secret Widget" not in response.data

def test_no_cross_org_data_leak_via_direct_id(client, db):
    """User can't access products from other orgs by ID."""
    # Create org A with product
    user_a = User.create(db, "a@example.com", "pass123", "Org A")
    org_a_id = user_a["organization_id"]
    
    product_id_a = db.products.insert_one({
        "organization_id": ObjectId(org_a_id),
        "name": "Org A Product",
        "sku": "A-001",
        "quantity_on_hand": 10
    }).inserted_id
    
    # Create org B + login
    client.post("/auth/signup", data={
        "email": "b@example.com",
        "password": "pass123",
        "org_name": "Org B"
    })
    
    # Try to access Org A's product
    response = client.get(f"/products/{product_id_a}/edit", follow_redirects=True)
    
    # Should fail or redirect
    assert response.status_code == 404 or b"not found" in response.data.lower()
