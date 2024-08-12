from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='client', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    item_value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

