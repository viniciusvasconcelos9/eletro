from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Order, Client, Menu, OrderItem
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('order_management'))

#------------------------------------------------------------
#ORDER MANAGEMENT
@app.route('/order_management')
def order_management():
    clients = Client.query.all()
    menu_items = Menu.query.all()
    return render_template('order_management.html', clients=clients, menu_items=menu_items)

@app.route('/order_management', methods=['POST'])
def create_order():
    data = request.form
    client_id = data['client_id']
    menu_item_ids = data.getlist('menu_item_ids')
    quantities = data.getlist('quantities')
    
    new_order = Order(
        client_id=client_id,
        status='Pending',
        value=0.0  # We'll calculate this later
    )
    
    db.session.add(new_order)
    db.session.flush()  # Get the new order ID before committing

    total_value = 0.0
    for menu_item_id, quantity in zip(menu_item_ids, quantities):
        quantity = int(quantity)
        menu_item = Menu.query.get(menu_item_id)
        total_value += menu_item.item_value * quantity
        
        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=menu_item_id,
            quantity=quantity
        )
        db.session.add(order_item)
    
    new_order.value = total_value
    db.session.commit()
    
    return redirect(url_for('orders'))
#------------------------------------------------------------

#------------------------------------------------------------
#CLIENTS
@app.route('/clients')
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.form
    new_client = Client(
        client_name=data['client_name'],
        address=data['address'],
        phone=data['phone']
    )

    db.session.add(new_client)
    db.session.commit()
    return redirect(url_for('clients'))

@app.route('/clients/<int:clients_id>/update', methods=['POST'])
def update_client(clients_id):
    client = Client.query.get(clients_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    data = request.form
    client.client_name = data.get('client_name', client.client_name)
    client.address = data.get('address', client.address)
    client.phone = data.get('phone', client.phone)

    db.session.commit()
    return redirect(url_for('clients'))

@app.route('/clients/<int:clients_id>/delete', methods=['POST'])
def delete_client(clients_id):
    client = Client.query.get(clients_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404

    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients'))
#------------------------------------------------------------

#------------------------------------------------------------
#ORDERS
@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/orders/<int:order_id>/update', methods=['POST'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.form
    order.status = data.get('status', order.status)
    db.session.commit()
    return redirect(url_for('orders'))

@app.route('/orders/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('orders'))
#------------------------------------------------------------

#------------------------------------------------------------
#MENU
@app.route('/menu')
def menu():
    items = Menu.query.all()
    return render_template('menu.html', menu=items)

@app.route('/menu', methods=['POST'])
def create_item():
    data = request.form
    new_item = Menu(
        item_name=data['item_name'],
        description=data['description'],
        item_value=data['item_value'],
        category=data['category']
    )

    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('menu'))

@app.route('/menu/<int:menu_id>/update', methods=['POST'])
def update_menu(menu_id):
    item = Menu.query.get(menu_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    data = request.form
    item.item_name = data.get('item_name', item.item_name)
    item.description = data.get('description', item.description)
    item.item_value = data.get('item_value', item.item_value)
    item.category = data.get('category', item.category)

    db.session.commit()
    return redirect(url_for('menu'))

@app.route('/menu/<int:menu_id>/delete', methods=['POST'])
def delete_item(menu_id):
    item = Menu.query.get(menu_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('menu'))
#------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
