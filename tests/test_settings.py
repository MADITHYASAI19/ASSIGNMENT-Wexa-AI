import pytest
from bson import ObjectId

def test_set_low_stock_threshold(client, auth_user, db):
    """Update default low-stock threshold."""
    org_id = auth_user["organization_id"]
    
    response = client.post("/settings/set-threshold", data={
        "threshold": "10"
    })
    
    org = db.organizations.find_one({"_id": ObjectId(org_id)})
    assert org["default_low_stock_threshold"] == 10
