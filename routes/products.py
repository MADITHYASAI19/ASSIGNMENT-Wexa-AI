from flask import Blueprint, render_template, request, session, redirect, url_for, g, jsonify
from models.product import Product
from functools import wraps
from bson import ObjectId

products_bp = Blueprint("products", __name__, url_prefix="/products")

def login_required(f):
    """Decorator to check session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@products_bp.route("/")
@login_required
def list_products():
    org_id = session["organization_id"]
    products = Product.list_by_org(g.db, org_id)
    return render_template("products/list.html", products=products)

@products_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        org_id = session["organization_id"]
        name = request.form.get("name", "").strip()
        sku = request.form.get("sku", "").strip()
        quantity = request.form.get("quantity", 0)
        cost_price = request.form.get("cost_price", None)
        selling_price = request.form.get("selling_price", None)
        low_stock_threshold = request.form.get("low_stock_threshold", None)
        
        # Validation
        errors = []
        if not name:
            errors.append("Product name required.")
        if not sku:
            errors.append("SKU required.")
        # Check SKU uniqueness per org
        if g.db.products.find_one({"organization_id": ObjectId(org_id), "sku": sku}):
            errors.append("SKU already exists in your org.")
        try:
            int(quantity)
        except:
            errors.append("Quantity must be a number.")
        
        if errors:
            return render_template("products/form.html", errors=errors), 400
        
        Product.create(g.db, org_id, name, sku, quantity, cost_price, selling_price, low_stock_threshold)
        return redirect(url_for("products.list_products"))
    
    return render_template("products/form.html")

@products_bp.route("/<product_id>/edit", methods=["GET", "POST"])
@login_required
def edit(product_id):
    org_id = session["organization_id"]
    product = Product.get_by_id(g.db, product_id, org_id)
    
    if not product:
        return "Product not found", 404
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        quantity = request.form.get("quantity", 0)
        selling_price = request.form.get("selling_price", None)
        low_stock_threshold = request.form.get("low_stock_threshold", None)
        
        Product.update(g.db, product_id, org_id,
            name=name,
            quantity_on_hand=int(quantity),
            selling_price=float(selling_price) if selling_price else None,
            low_stock_threshold=int(low_stock_threshold) if low_stock_threshold else None
        )
        return redirect(url_for("products.list_products"))
    
    return render_template("products/form.html", product=product, edit=True)

@products_bp.route("/<product_id>/delete", methods=["POST"])
@login_required
def delete(product_id):
    org_id = session["organization_id"]
    Product.delete(g.db, product_id, org_id)
    return redirect(url_for("products.list_products"))

@products_bp.route("/<product_id>/adjust", methods=["POST"])
@login_required
def adjust_quantity(product_id):
    try:
        data = request.get_json()
        delta = int(data.get("delta", 0))
        org_id = session["organization_id"]
        product = Product.get_by_id(g.db, product_id, org_id)
        if not product:
            return jsonify({"success": False, "error": "Product not found"}), 404
        
        new_qty = max(0, int(product.get("quantity_on_hand", 0)) + delta)
        Product.update(g.db, product_id, org_id, quantity_on_hand=new_qty)
        return jsonify({"success": True, "product_name": product.get("name"), "new_qty": new_qty})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
