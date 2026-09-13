import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for

from models import db, Supplier, Truck, Product, Route, Ticket


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)


# =========================================================
# DATABASE CONFIGURATION
# PostgreSQL only
# =========================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


required_variables = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}

missing_variables = [
    name
    for name, value in required_variables.items()
    if not value
]

if missing_variables:
    raise RuntimeError(
        "Missing database environment variables: "
        + ", ".join(missing_variables)
    )


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Connect SQLAlchemy with Flask
db.init_app(app)


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def dashboard():

    stats = {
        "trucks": Truck.query.count(),
        "suppliers": Supplier.query.count(),
        "products": Product.query.count(),
        "routes": Route.query.count(),
        "tickets": Ticket.query.count()
    }

    return render_template(
        "dashboard.html",
        stats=stats
    )


# =========================================================
# SUPPLIERS
# =========================================================

@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():

    if request.method == "POST":

        supplier = Supplier(
            name=request.form.get("name"),
            manager=request.form.get("manager"),
            phone=request.form.get("phone"),
            status=request.form.get(
                "status",
                "Active"
            )
        )

        db.session.add(supplier)
        db.session.commit()

        return redirect(url_for("suppliers"))

    suppliers_list = Supplier.query.order_by(
        Supplier.id.desc()
    ).all()

    return render_template(
        "suppliers.html",
        suppliers=suppliers_list
    )


# =========================================================
# TRUCKS
# =========================================================

@app.route("/trucks", methods=["GET", "POST"])
def trucks():

    if request.method == "POST":

        truck = Truck(
            registration=request.form.get(
                "registration"
            ),
            driver=request.form.get(
                "driver"
            ),
            capacity=float(
                request.form.get(
                    "capacity"
                ) or 0
            ),
            status=request.form.get(
                "status",
                "Available"
            )
        )

        db.session.add(truck)
        db.session.commit()

        return redirect(url_for("trucks"))

    trucks_list = Truck.query.order_by(
        Truck.id.desc()
    ).all()

    return render_template(
        "trucks.html",
        trucks=trucks_list
    )


# =========================================================
# PRODUCTS
# =========================================================

@app.route("/products", methods=["GET", "POST"])
def products():

    if request.method == "POST":

        supplier_id = request.form.get(
            "supplier_id"
        )

        product = Product(
            name=request.form.get("name"),
            sku=request.form.get("sku"),
            quantity=int(
                request.form.get("quantity") or 0
            ),
            supplier_id=(
                int(supplier_id)
                if supplier_id
                else None
            )
        )

        db.session.add(product)
        db.session.commit()

        return redirect(url_for("products"))

    products_list = Product.query.order_by(
        Product.id.desc()
    ).all()

    suppliers_list = Supplier.query.order_by(
        Supplier.name
    ).all()

    return render_template(
        "products.html",
        products=products_list,
        suppliers=suppliers_list
    )


# =========================================================
# ROUTES
# =========================================================

@app.route("/routes", methods=["GET", "POST"])
def routes():

    if request.method == "POST":

        truck_id = request.form.get(
            "truck_id"
        )

        route = Route(
            origin=request.form.get("origin"),
            destination=request.form.get("destination"),
            distance_km=float(
                request.form.get(
                    "distance_km"
                ) or 0
            ),
            selected=(
                request.form.get("selected") == "on"
            ),
            truck_id=(
                int(truck_id)
                if truck_id
                else None
            )
        )

        db.session.add(route)
        db.session.commit()

        return redirect(url_for("routes"))

    routes_list = Route.query.order_by(
        Route.id.desc()
    ).all()

    trucks_list = Truck.query.order_by(
        Truck.registration
    ).all()

    return render_template(
        "routes.html",
        routes=routes_list,
        trucks=trucks_list
    )


# =========================================================
# TICKETS
# =========================================================

@app.route("/tickets", methods=["GET", "POST"])
def tickets():

    if request.method == "POST":

        ticket = Ticket(
            title=request.form.get("title"),
            description=request.form.get("description"),
            priority=request.form.get(
                "priority",
                "Medium"
            ),
            status=request.form.get(
                "status",
                "Open"
            ),
            assignee=request.form.get("assignee"),
            jira_key=request.form.get("jira_key")
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for("tickets"))

    tickets_list = Ticket.query.order_by(
        Ticket.id.desc()
    ).all()

    return render_template(
        "tickets.html",
        tickets=tickets_list
    )


# =========================================================
# UPDATE TICKET STATUS
# =========================================================

@app.route(
    "/tickets/<int:ticket_id>/status",
    methods=["POST"]
)
def update_ticket_status(ticket_id):

    ticket = Ticket.query.get_or_404(
        ticket_id
    )

    new_status = request.form.get("status")

    if new_status:
        ticket.status = new_status
        db.session.commit()

    return redirect(
        url_for("tickets")
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    try:

        db.session.execute(
            db.text("SELECT 1")
        )

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as e:

        return jsonify({
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }), 500


# =========================================================
# API STATS
# =========================================================

@app.route("/api/stats")
def api_stats():

    return jsonify({
        "trucks": Truck.query.count(),
        "suppliers": Supplier.query.count(),
        "products": Product.query.count(),
        "routes": Route.query.count(),
        "tickets": Ticket.query.count()
    })


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )