from pymongo.errors import DuplicateKeyError
import bcrypt
from datetime import datetime

class User:
    @staticmethod
    def create(db, email, password, org_name):
        """Create user + organization."""
        # Hash password
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Create org first
        org = db.organizations.insert_one({
            "name": org_name,
            "default_low_stock_threshold": 5
        })
        org_id = org.inserted_id
        
        # Create user
        try:
            user = db.users.insert_one({
                "email": email,
                "password_hash": hashed,
                "organization_id": org_id,
                "created_at": datetime.utcnow()
            })
            return {"_id": str(user.inserted_id), "organization_id": str(org_id), "email": email}
        except DuplicateKeyError:
            db.organizations.delete_one({"_id": org_id})  # Rollback org
            return None

    @staticmethod
    def verify_login(db, email, password):
        """Check email + password, return user if valid."""
        user = db.users.find_one({"email": email})
        if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return None
        return {
            "_id": str(user["_id"]),
            "email": user["email"],
            "organization_id": str(user["organization_id"])
        }

    @staticmethod
    def get_by_id(db, user_id):
        """Fetch user by ID."""
        from bson import ObjectId
        return db.users.find_one({"_id": ObjectId(user_id)})
