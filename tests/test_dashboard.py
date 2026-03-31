import pytest
from bson import ObjectId

def test_dashboard_shows_totals(client, auth_user, db):
    """Dashboard shows total products and inventory."""
    org_id = auth_user["organization_id"]
    
    # Create 3 products
    for i in range(3):
        db.products.insert_one({
            "organization_id": ObjectId(org_id),
            "name": f"Product {i}",
            "sku": f"SKU-{i}",
            "quantity_on_hand": 5 + i
        })
    
    response = client.get("/", follow_redirects=True)
    assert b"3" in response.data  # Total products
    assert b"18" in response.data  # Total inventory (5+6+7)

def test_dashboard_shows_low_stock(client, auth_user, db):
    """Dashboard shows low-stock items."""
    org_id = auth_user["organization_id"]
    
    # Set org default threshold to 5
    db.organizations.update_one(
        {"_id": ObjectId(org_id)},
        {"$set": {"default_low_stock_threshold": 5}}
    )
    
    # Create product with qty=3 (below threshold)
    db.products.insert_one({
        "organization_id": ObjectId(org_id),
        "name": "Low Stock Widget",
        "sku": "LOW-001",
        "quantity_on_hand": 3
    })
    
    response = client.get("/", follow_redirects=True)
    assert b"Low Stock Widget" in response.data
