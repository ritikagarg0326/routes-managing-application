from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Supplier(db.Model):
    __tablename__ = "supplier"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manager = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    status = db.Column(db.String(50))

    products = db.relationship(
        "Product",
        backref="supplier",
        lazy=True
    )


class Truck(db.Model):
    __tablename__ = "truck"

    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    driver = db.Column(db.String(100))
    capacity = db.Column(db.Float)
    status = db.Column(db.String(50))

    routes = db.relationship(
        "Route",
        backref="truck",
        lazy=True
    )


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False
    )
    sku = db.Column(db.String(100))
    quantity = db.Column(
        db.Integer,
        default=0
    )

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("supplier.id")
    )


class Route(db.Model):
    __tablename__ = "route"

    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    distance_km = db.Column(db.Float)

    selected = db.Column(
        db.Boolean,
        default=False
    )

    truck_id = db.Column(
        db.Integer,
        db.ForeignKey("truck.id")
    )


class Ticket(db.Model):
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(200),
        nullable=False
    )
    description = db.Column(db.Text)
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50))
    assignee = db.Column(db.String(100))
    jira_key = db.Column(db.String(100))