from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Order,Clients
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
    return render_template('order_management.html')
#------------------------------------------------------------

#------------------------------------------------------------
#CLIENTS
@app.route('/clients')
def clients():
    clients = Clients.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.form
    new_client = Clients(
        client_name=data['client_name'],
        address=data['address'],
        phone=data['phone']
    )

    db.session.add(new_client)
    db.session.commit()
    return redirect(url_for('clients'))

@app.route('/clients/<int:clients_id>/update', methods=['POST'])
def update_client(clients_id):
    client = Clients.query.get(clients_id)
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
    client = Clients.query.get(clients_id)
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

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.form
    new_order = Order(
        client_name=data['client_name'],
        date=datetime.strptime(data['date'], '%Y-%m-%d'),
        description=data['description'],
        value=data['value'],
        status='Aguardando',
        order_type=data['order_type']  # Set order type
    )
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('orders'))

@app.route('/orders/<int:order_id>/update', methods=['POST'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.form
    order.status = data.get('status', order.status)
    order.client_name = data.get('client_name', order.client_name)
    order.date = datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else order.date
    order.value = data.get('value', order.value)
    order.description = data.get('description', order.description)
    order.order_type = data.get('order_type', order.order_type)  # Update order type

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
#FINANCE
@app.route('/finance')
def finance():
    return render_template('finance.html')
#------------------------------------------------------------
 
#------------------------------------------------------------
#EXPENSES
@app.route('/expenses')
def expenses():
    return render_template('expenses.html')
#------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
