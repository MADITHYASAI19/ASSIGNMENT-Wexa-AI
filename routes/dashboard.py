from flask import Blueprint, render_template, session, g, redirect, url_for
from models.product import Product
from functools import wraps

dashboard_bp = Blueprint("dashboard", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route("/")
@login_required
def index():
    org_id = session["organization_id"]
    
    # Fetch all products for org
    all_products = Product.list_by_org(g.db, org_id)
    
    # Calculate totals
    total_products = len(all_products)
    total_inventory = sum(p.get("quantity_on_hand", 0) for p in all_products)
    
    # Get low-stock items
    low_stock_items = Product.get_low_stock_items(g.db, org_id)
    
    # Aggregate Stats
    total_val = sum((p.get("quantity_on_hand", 0) * p.get("selling_price", 0)) for p in all_products)
    
    # Activity Feed (Fetch from DB if exists, otherwise mock)
    from bson import ObjectId
    activities = list(g.db.activity_log.find({"organization_id": ObjectId(org_id)}).sort("timestamp", -1).limit(10))
    
    return render_template("dashboard.html",
        stats={
            "total_products": total_products,
            "total_value": "{:,.0f}".format(total_val),
            "low_stock_count": len(low_stock_items)
        },
        low_stock_products=low_stock_items,
        activities=activities
    )
