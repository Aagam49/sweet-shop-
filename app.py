from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'aagam_sweet_shop_2025'


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sweets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Sweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Sweet {self.name}>"

# Create DB if not exists
with app.app_context():
    if not os.path.exists("sweets.db"):
        db.create_all()

# Home route with sorting and pagination
@app.route('/')
def index():
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    query = Sweet.query

    if sort_by == 'name_asc':
        query = query.order_by(Sweet.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Sweet.name.desc())
    elif sort_by == 'price_asc':
        query = query.order_by(Sweet.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Sweet.price.desc())
    elif sort_by == 'quantity_asc':
        query = query.order_by(Sweet.quantity.asc())
    elif sort_by == 'quantity_desc':
        query = query.order_by(Sweet.quantity.desc())

    sweets_paginated = query.paginate(page=page, per_page=5)
    return render_template('index.html', sweets=sweets_paginated.items, pagination=sweets_paginated)

# Add sweet
@app.route('/add', methods=['POST'])
def add_sweet():
    id = int(request.form['id'])
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])

    existing = Sweet.query.get(id)
    if existing:
        return redirect('/')

    sweet = Sweet(id=id, name=name, category=category, price=price, quantity=quantity)
    db.session.add(sweet)
    db.session.commit()
    return redirect('/')

# Delete sweet
@app.route('/delete/<int:sweet_id>', methods=['POST'])
def delete_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if sweet:
        db.session.delete(sweet)
        db.session.commit()
    return redirect('/')

# Restock sweet
@app.route('/restock/<int:sweet_id>', methods=['POST'])
def restock_sweet(sweet_id):
    qty = int(request.form['restock_qty'])
    sweet = Sweet.query.get(sweet_id)
    if sweet:
        sweet.quantity += qty
        db.session.commit()
    return redirect('/')

# Search sweets by name
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = Sweet.query.filter(Sweet.name.ilike(f"%{query}%")).all()
    return render_template('index.html', sweets=results, pagination=None)

@app.route('/customer')
def customer():
    sweets = Sweet.query.filter(Sweet.quantity > 0).all()
    return render_template('customer.html', sweets=sweets)

@app.route('/add_to_cart/<int:sweet_id>', methods=['POST'])
def add_to_cart(sweet_id):
    qty = int(request.form['qty'])
    sweet = Sweet.query.get(sweet_id)
    if not sweet or sweet.quantity < qty:
        return redirect('/customer')

    cart = session.get('cart', {})
    if str(sweet_id) in cart:
        cart[str(sweet_id)]['quantity'] += qty
    else:
        cart[str(sweet_id)] = {
            'id': sweet.id,
            'name': sweet.name,
            'price': sweet.price,
            'quantity': qty
        }
    session['cart'] = cart
    return redirect('/customer')

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove_from_cart/<int:sweet_id>', methods=['POST'])
def remove_from_cart(sweet_id):
    cart = session.get('cart', {})
    cart.pop(str(sweet_id), None)
    session['cart'] = cart
    return redirect('/cart')

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    for sweet_id, item in cart.items():
        sweet = Sweet.query.get(int(sweet_id))
        if sweet and sweet.quantity >= item['quantity']:
            sweet.quantity -= item['quantity']
        else:
            return "Insufficient stock for some items!"
    db.session.commit()
    session['cart'] = {}
    return redirect('/customer')

if __name__ == '__main__':
    app.run(debug=True)

