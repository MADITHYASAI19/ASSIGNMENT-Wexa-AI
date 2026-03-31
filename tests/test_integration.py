import pytest

def test_full_user_journey(client, db):
    """Complete flow: signup → create product → see on dashboard."""
    # Signup
    response = client.post("/auth/signup", data={
        "email": "journey@example.com",
        "password": "password123",
        "org_name": "Journey Org"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify on dashboard (empty state)
    assert b"0" in response.data  # 0 products
    
    # Create product
    response = client.post("/products/create", data={
        "name": "Test Widget",
        "sku": "TEST-001",
        "quantity": "7",
        "selling_price": "29.99"
    }, follow_redirects=True)
    
    # Check dashboard
    response = client.get("/", follow_redirects=True)
    assert b"Test Widget" in response.data
    assert b"1" in response.data  # 1 product
    
    # Create low-stock item
    client.post("/products/create", data={
        "name": "Low Stock Item",
        "sku": "LOW-001",
        "quantity": "2",
        "low_stock_threshold": "5"
    })
    
    # Check low-stock section
    response = client.get("/", follow_redirects=True)
    assert b"Low Stock Item" in response.data
