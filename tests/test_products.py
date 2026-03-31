import pytest
from models.product import Product
from bson import ObjectId

def test_create_product(client, auth_user):
    """Create a product."""
    org_id = auth_user["organization_id"]
    
    response = client.post("/products/create", data={
        "name": "Widget",
        "sku": "WGT-001",
        "quantity": "10",
        "cost_price": "5.00",
        "selling_price": "15.00"
    })
    
    assert response.status_code == 302  # Redirect after create
    # Verify in DB
    product = client.application.db.products.find_one({"sku": "WGT-001"})
    assert product is not None
    assert product["quantity_on_hand"] == 10

def test_list_products(client, auth_user, db):
    """List products for logged-in user."""
    org_id = auth_user["organization_id"]
    
    # Create 3 products
    for i in range(3):
        db.products.insert_one({
            "organization_id": ObjectId(org_id),
            "name": f"Product {i}",
            "sku": f"SKU-{i}",
            "quantity_on_hand": 10 + i
        })
    
    response = client.get("/products/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Product 0" in response.data
    assert b"Product 1" in response.data

def test_sku_uniqueness_per_org(client, auth_user, db):
    """SKU must be unique per org."""
    org_id = auth_user["organization_id"]
    
    # Create first product
    client.post("/products/create", data={
        "name": "Product 1",
        "sku": "DUP-001",
        "quantity": "5"
    })
    
    # Try to create duplicate SKU
    response = client.post("/products/create", data={
        "name": "Product 2",
        "sku": "DUP-001",
        "quantity": "10"
    })
    
    assert b"already exists" in response.data

def test_update_product(client, auth_user, db):
    """Edit product quantity."""
    org_id = auth_user["organization_id"]
    
    product_id = db.products.insert_one({
        "organization_id": ObjectId(org_id),
        "name": "Widget",
        "sku": "WGT-001",
        "quantity_on_hand": 10
    }).inserted_id
    
    response = client.post(f"/products/{product_id}/edit", data={
        "name": "Widget",
        "quantity": "5",
        "selling_price": "20.00"
    })
    
    updated = db.products.find_one({"_id": product_id})
    assert updated["quantity_on_hand"] == 5

def test_delete_product(client, auth_user, db):
    """Delete product."""
    org_id = auth_user["organization_id"]
    
    product_id = db.products.insert_one({
        "organization_id": ObjectId(org_id),
        "name": "Widget",
        "sku": "WGT-001",
        "quantity_on_hand": 10
    }).inserted_id
    
    response = client.post(f"/products/{product_id}/delete")
    
    assert db.products.find_one({"_id": product_id}) is None
