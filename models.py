from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    order_type = db.Column(db.String(20), nullable=False)  # New field

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    item_value = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    