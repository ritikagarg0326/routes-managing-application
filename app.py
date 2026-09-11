import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///logistics.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    manager = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    status = db.Column(db.String(30), default="Active")

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(40), unique=True, nullable=False)
    driver = db.Column(db.String(120))
    capacity = db.Column(db.Float, default=0)
    status = db.Column(db.String(30), default="Available")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"))
    supplier = db.relationship("Supplier")

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    distance_km = db.Column(db.Float, default=0)
    selected = db.Column(db.Boolean, default=False)
    truck_id = db.Column(db.Integer, db.ForeignKey("truck.id"))
    truck = db.relationship("Truck")

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(30), default="Medium")
    status = db.Column(db.String(30), default="Open")
    assignee = db.Column(db.String(120))
    jira_key = db.Column(db.String(40))

@app.route("/")
def dashboard():
    stats = {
        "trucks": Truck.query.count(),
        "routes": Route.query.count(),
        "suppliers": Supplier.query.count(),
        "products": Product.query.count(),
        "open_tickets": Ticket.query.filter(Ticket.status != "Done").count(),
    }
    return render_template("dashboard.html", stats=stats, tickets=Ticket.query.order_by(Ticket.id.desc()).limit(8).all())

@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    if request.method == "POST":
        db.session.add(Supplier(
            name=request.form["name"], manager=request.form.get("manager"),
            phone=request.form.get("phone")
        ))
        db.session.commit()
        flash("Supplier added.", "success")
        return redirect(url_for("suppliers"))
    return render_template("suppliers.html", suppliers=Supplier.query.order_by(Supplier.id.desc()).all())

@app.route("/trucks", methods=["GET", "POST"])
def trucks():
    if request.method == "POST":
        db.session.add(Truck(
            registration=request.form["registration"],
            driver=request.form.get("driver"),
            capacity=float(request.form.get("capacity") or 0),
        ))
        db.session.commit()
        flash("Truck added.", "success")
        return redirect(url_for("trucks"))
    return render_template("trucks.html", trucks=Truck.query.order_by(Truck.id.desc()).all())

@app.route("/products", methods=["GET", "POST"])
def products():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    if request.method == "POST":
        db.session.add(Product(
            name=request.form["name"], sku=request.form["sku"],
            quantity=int(request.form.get("quantity") or 0),
            supplier_id=int(request.form["supplier_id"]) if request.form.get("supplier_id") else None
        ))
        db.session.commit()
        flash("Product added.", "success")
        return redirect(url_for("products"))
    return render_template("products.html", products=Product.query.order_by(Product.id.desc()).all(), suppliers=suppliers)

@app.route("/routes", methods=["GET", "POST"])
def routes():
    trucks = Truck.query.filter_by(status="Available").all()
    if request.method == "POST":
        db.session.add(Route(
            origin=request.form["origin"], destination=request.form["destination"],
            distance_km=float(request.form.get("distance_km") or 0),
            selected=request.form.get("selected") == "on",
            truck_id=int(request.form["truck_id"]) if request.form.get("truck_id") else None
        ))
        db.session.commit()
        flash("Route added.", "success")
        return redirect(url_for("routes"))
    return render_template("routes.html", routes=Route.query.order_by(Route.id.desc()).all(), trucks=trucks)

@app.route("/tickets", methods=["GET", "POST"])
def tickets():
    if request.method == "POST":
        ticket = Ticket(
            title=request.form["title"], description=request.form.get("description"),
            priority=request.form.get("priority", "Medium"),
            assignee=request.form.get("assignee"),
            jira_key=request.form.get("jira_key")
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket created.", "success")
        return redirect(url_for("tickets"))
    return render_template("tickets.html", tickets=Ticket.query.order_by(Ticket.id.desc()).all())

@app.post("/tickets/<int:ticket_id>/status")
def ticket_status(ticket_id):
    ticket = db.get_or_404(Ticket, ticket_id)
    ticket.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("tickets"))

@app.get("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "logistics-app"})

@app.get("/api/stats")
def api_stats():
    return jsonify({
        "trucks": Truck.query.count(),
        "routes": Route.query.count(),
        "suppliers": Supplier.query.count(),
        "products": Product.query.count(),
        "open_tickets": Ticket.query.filter(Ticket.status != "Done").count()
    })

def seed():
    if Supplier.query.count():
        return
    s1 = Supplier(name="NorthStar Logistics", manager="Amit Sharma", phone="+91-9000000001")
    s2 = Supplier(name="FastMove Transport", manager="Neha Singh", phone="+91-9000000002")
    t1 = Truck(registration="DL01AB1234", driver="Rahul", capacity=12)
    t2 = Truck(registration="DL02CD5678", driver="Vikas", capacity=20)
    db.session.add_all([s1, s2, t1, t2])
    db.session.flush()
    db.session.add_all([
        Product(name="Engine Oil", sku="OIL-100", quantity=120, supplier=s1),
        Product(name="Brake Pads", sku="BRK-200", quantity=75, supplier=s2),
        Route(origin="Delhi", destination="Jaipur", distance_km=280, selected=True, truck=t1),
        Route(origin="Delhi", destination="Chandigarh", distance_km=245, selected=False, truck=t2),
        Ticket(title="High ECS CPU alert", description="Investigate sustained CPU above threshold", priority="High", status="In Progress", assignee="DevOps", jira_key="LOG-101"),
        Ticket(title="Add new supplier", description="Onboard supplier into application", priority="Medium", assignee="Operations", jira_key="LOG-102")
    ])
    db.session.commit()

with app.app_context():
    db.create_all()
    seed()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG", "0") == "1")
