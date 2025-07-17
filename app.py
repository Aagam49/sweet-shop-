from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
