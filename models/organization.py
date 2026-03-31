class Organization:
    @staticmethod
    def get_by_id(db, org_id):
        """Fetch org settings."""
        from bson import ObjectId
        return db.organizations.find_one({"_id": ObjectId(org_id)})

    @staticmethod
    def set_low_stock_threshold(db, org_id, threshold):
        """Update default threshold."""
        from bson import ObjectId
        db.organizations.update_one(
            {"_id": ObjectId(org_id)},
            {"$set": {"default_low_stock_threshold": int(threshold)}}
        )
