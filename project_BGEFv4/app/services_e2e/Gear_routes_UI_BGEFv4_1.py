
#Gear Model

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Gear Model
class Gear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

#Service Functions
#Create Gear

from flask import request, jsonify

@app.route('/gear', methods=['POST'])
def create_gear():
    data = request.get_json()
    new_gear = Gear(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_gear)
    db.session.commit()
    return jsonify({'message': 'New gear created!'}), 201

#Fetch All Gears

@app.route('/gears', methods=['GET'])
def get_all_gears():
    gears = Gear.query.all()
    output = []
    for gear in gears:
        gear_data = {
            'id': gear.id,
            'name': gear.name,
            'description': gear.description,
            'price': gear.price,
            'quantity': gear.quantity
        }
        output.append(gear_data)
    return jsonify({'gears': output})

#Fetch One Gear

@app.route('/gear/<gear_id>', methods=['GET'])
def get_one_gear(gear_id):
    gear = Gear.query.get(gear_id)
    if not gear:
        return jsonify({'message': 'Gear not found!'}), 404

    gear_data = {
        'id': gear.id,
        'name': gear.name,
        'description': gear.description,
        'price': gear.price,
        'quantity': gear.quantity
    }
    return jsonify({'gear': gear_data})

#Update Gear

@app.route('/gear/<gear_id>', methods=['PUT'])
def update_gear(gear_id):
    data = request.get_json()
    gear = Gear.query.get(gear_id)
    if not gear:
        return jsonify({'message': 'Gear not found!'}), 404

    gear.name = data['name']
    gear.description = data.get('description')
    gear.price = data['price']
    gear.quantity = data['quantity']

    db.session.commit()
    return jsonify({'message': 'Gear updated!'})

#Delete Gear

@app.route('/gear/<gear_id>', methods=['DELETE'])
def delete_gear(gear_id):
    gear = Gear.query.get(gear_id)
    if not gear:
        return jsonify({'message': 'Gear not found!'}), 404

    db.session.delete(gear)
    db.session.commit()
    return jsonify({'message': 'Gear deleted!'})

#Controller Components
#Gear Controller

from flask import Blueprint, render_template, request, redirect, url_for

gear_bp = Blueprint('gear_bp', __name__)

@gear_bp.route('/gears', methods=['GET'])
def gears():
    gears = Gear.query.all()
    return render_template('gears.html', gears=gears)

@gear_bp.route('/gear/<gear_id>', methods=['GET'])
def gear(gear_id):
    gear = Gear.query.get(gear_id)
    if not gear:
        return render_template('404.html'), 404
    return render_template('gear.html', gear=gear)

@gear_bp.route('/gear/new', methods=['GET', 'POST'])
def new_gear():
    if request.method == 'POST':
        data = request.form
        new_gear = Gear(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            quantity=data['quantity']
        )
        db.session.add(new_gear)
        db.session.commit()
        return redirect(url_for('gear_bp.gears'))
    return render_template('new_gear.html')

@gear_bp.route('/gear/edit/<gear_id>', methods=['GET', 'POST'])
def edit_gear(gear_id):
    gear = Gear.query.get(gear_id)
    if not gear:
        return render_template('404.html'), 404
    if request.method == 'POST':
        data = request.form
        gear.name = data['name']
        gear.description = data.get('description')
        gear.price = data['price']
        gear.quantity = data['quantity']
        db.session.commit()
        return redirect(url_for('gear_bp.gears'))
    return render_template('edit_gear.html', gear=gear)

@gear_bp.route('/gear/delete/<gear_id>', methods=['POST'])
def delete_gear(gear_id):
    gear = Gear.query.get(gear_id)
    if not gear:
        return render_template('404.html'), 404
    db.session.delete(gear)
    db.session.commit()
    return redirect(url_for('gear_bp.gears'))

#UI Pages with Jinja2 Templates, HTML, and Bootstrap
#gears.html

{% extends "base.html" %}

{% block title %}Gears{% endblock %}

{% block content %}
    <h1 class="mt-5">Gears</h1>
    <a href="{{ url_for('gear_bp.new_gear') }}" class="btn btn-primary mb-3">Add New Gear</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for gear in gears %}
            <tr>
                <td>{{ gear.id }}</td>
                <td>{{ gear.name }}</td>
                <td>{{ gear.description }}</td>
                <td>{{ gear.price }}</td>
                <td>{{ gear.quantity }}</td>
                <td>
                    <a href="{{ url_for('gear_bp.gear', gear_id=gear.id) }}" class="btn btn-info btn-sm">View</
                    <a href="{{ url_for('gear_bp.edit_gear', gear_id=gear.id) }}" class="btn btn-warning
btn-sm">Edit</a>
                    <form action="{{ url_for('gear_bp.delete_gear', gear_id=gear.id) }}" method="post"
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#gear.html

{% extends "base.html" %}

{% block title %}Gear Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Gear Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ gear.id }}</td>
        </tr>
        <tr>
            <th>Name</th>
            <td>{{ gear.name }}</td>
        </tr>
        <tr>
            <th>Description</th>
            <td>{{ gear.description }}</td>
        </tr>
        <tr>
            <th>Price</th>
            <td>{{ gear.price }}</td>
        </tr>
        <tr>
            <th>Quantity</th>
            <td>{{ gear.quantity }}</td>
        </tr>
    </table>
    <a href="{{ url_for('gear_bp.gears') }}" class="btn btn-secondary">Back to Gears</a>
{% endblock %}

#new_gear.html

{% extends "base.html" %}

{% block title %}New Gear{% endblock %}

{% block content %}
    <h1 class="mt-5">Add New Gear</h1>
    <form action="{{ url_for('gear_bp.new_gear') }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description"></textarea>
        </div>
        <div class="form-group">
            <label for="price">Price</label>
            <input type="number" step="0.01" class="form-control" id="price" name="price" required>
        </div>
        <div class="form-group">
            <label for="quantity">Quantity</label>
            <input type="number" class="form-control" id="quantity" name="quantity" required>
        </div>
        <button type="submit" class="btn btn-primary">Add Gear</button>
    </form>
{% endblock %}

#edit_gear.html

{% extends "base.html" %}

{% block title %}Edit Gear{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit Gear</h1>
    <form action="{{ url_for('gear_bp.edit_gear', gear_id=gear.id) }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name" value="{{ gear.name }}">
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description">{{ gear.description }}</textarea
        </div>
        <div class="form-group">
            <label for="category">Category</label>
            <input type="text" class="form-control" id="category" name="category" value="{{ gear.category }}">
        </div>
        <button type="submit" class="btn btn-primary">Save</button>
    </form>
{% endblock %}

#add_gear.html

{% extends "base.html" %}

{% block title %}Add Gear{% endblock %}

{% block content %}
    <h1 class="mt-5">Add Gear</h1>
    <form action="{{ url_for('gear_bp.add_gear') }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name">
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description"></textarea>
        </div>
        <div class="form-group">
            <label for="category">Category</label>
            <input type="text" class="form-control" id="category" name="category">
        </div>
        <button type="submit" class="btn btn-primary">Add</button>
    </form>
{% endblock %}

#view_gear.html

{% extends "base.html" %}

{% block title %}View Gear{% endblock %}

{% block content %}
    <h1 class="mt-5">Gear Details</h1>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{{ gear.name }}</h5>
            <p class="card-text">{{ gear.description }}</p>
            <p class="card-text"><strong>Category:</strong> {{ gear.category }}</p>
            <a href="{{ url_for('gear_bp.edit_gear', gear_id=gear.id) }}" class="btn btn-primary">Edit</a>
            <a href="{{ url_for('gear_bp.delete_gear', gear_id=gear.id) }}" class="btn btn-danger">Delete</a>
        </div>
    </div>
{% endblock %}

#list_gear.html

{% extends "base.html" %}

{% block title %}Gear List{% endblock %}

{% block content %}
    <h1 class="mt-5">Gear List</h1>
    <a href="{{ url_for('gear_bp.add_gear') }}" class="btn btn-primary mb-3">Add Gear</a>
    <ul class="list-group">
        {% for gear in gears %}
            <li class="list-group-item">
                <a href="{{ url_for('gear_bp.view_gear', gear_id=gear.id) }}">{{ gear.name }}</a>
            </li>
        {% endfor %}
    </ul>
{% endblock %