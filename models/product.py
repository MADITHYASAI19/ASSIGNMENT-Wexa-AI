from bson import ObjectId
from datetime import datetime

class Product:
    @staticmethod
    def create(db, org_id, name, sku, quantity, cost_price=None, selling_price=None, low_stock_threshold=None):
        """Create product."""
        return db.products.insert_one({
            "organization_id": ObjectId(org_id),
            "name": name,
            "sku": sku,
            "description": "",
            "quantity_on_hand": int(quantity),
            "cost_price": float(cost_price) if cost_price else None,
            "selling_price": float(selling_price) if selling_price else None,
            "low_stock_threshold": int(low_stock_threshold) if low_stock_threshold else None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }).inserted_id

    @staticmethod
    def list_by_org(db, org_id, skip=0, limit=100):
        """Fetch all products for org."""
        return list(db.products.find(
            {"organization_id": ObjectId(org_id)}
        ).skip(skip).limit(limit).sort("created_at", -1))

    @staticmethod
    def get_by_id(db, product_id, org_id):
        """Fetch single product (verify org ownership)."""
        return db.products.find_one({
            "_id": ObjectId(product_id),
            "organization_id": ObjectId(org_id)
        })

    @staticmethod
    def update(db, product_id, org_id, **fields):
        """Update product fields."""
        result = db.products.update_one(
            {"_id": ObjectId(product_id), "organization_id": ObjectId(org_id)},
            {"$set": {**fields, "updated_at": datetime.utcnow()}}
        )
        return result.matched_count > 0

    @staticmethod
    def delete(db, product_id, org_id):
        """Hard delete product."""
        result = db.products.delete_one({
            "_id": ObjectId(product_id),
            "organization_id": ObjectId(org_id)
        })
        return result.deleted_count > 0

    @staticmethod
    def get_low_stock_items(db, org_id):
        """Fetch products where quantity <= threshold."""
        from models.organization import Organization
        org = Organization.get_by_id(db, org_id)
        default_threshold = org.get("default_low_stock_threshold", 5) if org else 5
        
        return list(db.products.find({
            "organization_id": ObjectId(org_id),
            "$expr": {
                "$lte": [
                    "$quantity_on_hand",
                    {"$ifNull": ["$low_stock_threshold", default_threshold]}
                ]
            }
        }))
