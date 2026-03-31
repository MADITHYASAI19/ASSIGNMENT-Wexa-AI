import os
from pymongo import MongoClient
import bcrypt
from datetime import datetime
from bson import ObjectId

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/stockflow")
client = MongoClient(MONGO_URI)
db = client["stockflow"]

def clear_db():
    print("Clearing existing data...")
    db.users.delete_many({})
    db.organizations.delete_many({})
    db.products.delete_many({})

def create_org_and_user(org_name, email, password):
    """Creates an organization and its admin user."""
    # Create Organization
    org = db.organizations.insert_one({
        "name": org_name,
        "default_low_stock_threshold": 5
    })
    org_id = org.inserted_id
    
    # Create User
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = db.users.insert_one({
        "email": email,
        "password_hash": hashed,
        "organization_id": org_id,
        "created_at": datetime.utcnow()
    })
    print(f"Created Org: {org_name} | User: {email} (Password: {password})")
    return org_id

def create_products(org_id, products_data):
    """Creates products for a specific organization."""
    for p in products_data:
        db.products.insert_one({
            "organization_id": org_id,
            "name": p["name"],
            "sku": p["sku"],
            "description": p.get("description", ""),
            "quantity_on_hand": p["qty"],
            "cost_price": p.get("cost"),
            "selling_price": p.get("sell"),
            "low_stock_threshold": p.get("threshold", 5),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
    print(f"Added {len(products_data)} products for org {org_id}")

if __name__ == "__main__":
    clear_db()
    
    # 1. Stark Industries (Org 1)
    stark_org_id = create_org_and_user(
        org_name="Stark Industries",
        email="tony@stark.com",
        password="password123"
    )
    stark_products = [
        {"name": "Iron Man Suit Mark I", "sku": "MK-001", "qty": 1, "cost": 1000000, "sell": 5000000, "threshold": 2},
        {"name": "Arc Reactor Generator", "sku": "ARC-100", "qty": 10, "cost": 500, "sell": 2000, "threshold": 5},
        {"name": "Repulsor Glove", "sku": "REP-055", "qty": 3, "cost": 1500, "sell": 4500, "threshold": 5}, # Low stock
        {"name": "Vibranium Shield Prototype", "sku": "VIB-001", "qty": 0, "cost": 10000, "sell": 50000, "threshold": 1}, # Low stock
    ]
    create_products(stark_org_id, stark_products)

    # 2. Wayne Enterprises (Org 2)
    wayne_org_id = create_org_and_user(
        org_name="Wayne Enterprises",
        email="bruce@wayne.com",
        password="password123"
    )
    wayne_products = [
        {"name": "Batarang Pack (10x)", "sku": "BAT-010", "qty": 50, "cost": 20, "sell": 100},
        {"name": "Grapple Gun", "sku": "GRP-002", "qty": 12, "cost": 250, "sell": 800},
        {"name": "Smoke Pellets Box", "sku": "SMK-999", "qty": 4, "cost": 5, "sell": 30, "threshold": 10}, # Low stock
    ]
    create_products(wayne_org_id, wayne_products)
    
    print("\n--- SEEDING COMPLETE ---")
    print("You can now log in with the following accounts:")
    print("1. tony@stark.com / password123")
    print("2. bruce@wayne.com / password123")
