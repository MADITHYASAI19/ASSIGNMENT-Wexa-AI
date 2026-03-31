from flask import Blueprint, render_template, session, g, redirect, url_for, jsonify
from functools import wraps
from collections import defaultdict

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@analytics_bp.route("/")
@login_required
def index():
    org_id = session["organization_id"]
    
    # Get all products for this organization
    products = list(g.db.products.find({"organization_id": org_id}))
    
    # Calculate category distribution
    category_data = defaultdict(int)
    total_value_by_month = [0] * 6
    product_performance = []
    
    for product in products:
        # Category distribution
        category = product.get("category", "Uncategorized")
        qty = product.get("quantity_on_hand", 0)
        category_data[category] += qty
        
        # Product performance (turnover simulation based on stock levels)
        performance = min(100, max(10, qty * 5)) if qty > 0 else 0
        product_performance.append({
            "name": product.get("name", "Unknown"),
            "turnover": performance
        })
    
    # Sort and limit performance data
    product_performance = sorted(product_performance, key=lambda x: x["turnover"], reverse=True)[:6]
    
    # Calculate total inventory value trend (simulated 6-month trend)
    base_value = sum(p.get("selling_price", 0) * p.get("quantity_on_hand", 0) for p in products)
    trend_data = [
        base_value * 0.7,
        base_value * 0.8,
        base_value * 0.85,
        base_value * 0.9,
        base_value * 0.95,
        base_value
    ]
    
    # Prepare chart data
    chart_data = {
        "distribution": {
            "labels": list(category_data.keys()) or ["No Data"],
            "data": list(category_data.values()) or [1]
        },
        "trend": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "data": trend_data
        },
        "performance": {
            "labels": [p["name"] for p in product_performance],
            "data": [p["turnover"] for p in product_performance]
        }
    }
    
    return render_template("analytics/dashboard.html", chart_data=chart_data, products_count=len(products))

@analytics_bp.route("/api/stats")
@login_required
def api_stats():
    """API endpoint for real-time chart updates."""
    org_id = session["organization_id"]
    products = list(g.db.products.find({"organization_id": org_id}))
    
    total_value = sum(p.get("selling_price", 0) * p.get("quantity_on_hand", 0) for p in products)
    low_stock = sum(1 for p in products if p.get("quantity_on_hand", 0) <= p.get("low_stock_threshold", 5))
    
    return jsonify({
        "total_products": len(products),
        "total_value": round(total_value, 2),
        "low_stock_count": low_stock
    })
