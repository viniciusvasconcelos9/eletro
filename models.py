from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    order_type = db.Column(db.String(20), nullable=False) 
    items = db.relationship('OrderItem', backref='order', lazy=True)
    client = db.relationship('Clients', backref='orders')  # Relation to Clients

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_value = db.Column(db.Float, nullable=False)

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    item_value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)
