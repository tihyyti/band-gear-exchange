
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#BidGenre Model
class BidGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

#Service Functions
#Create BidGenre

from flask import request, jsonify

@app.route('/bidgenre', methods=['POST'])
def create_bidgenre():
    data = request.get_json()
    new_bidgenre = BidGenre(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(new_bidgenre)
    db.session.commit()
    return jsonify({'message': 'New bid genre created!'}), 201

#Fetch All BidGenres

@app.route('/bidgenres', methods=['GET'])
def get_all_bidgenres():
    bidgenres = BidGenre.query.all()
    output = []
    for bidgenre in bidgenres:
        bidgenre_data = {
            'id': bidgenre.id,
            'name': bidgenre.name,
            'description': bidgenre.description
        }
        output.append(bidgenre_data)
    return jsonify({'bidgenres': output})

#Fetch One BidGenre

@app.route('/bidgenre/<bidgenre_id>', methods=['GET'])
def get_one_bidgenre(bidgenre_id):
    bidgenre = BidGenre.query.get(bidgenre_id)
    if not bidgenre:
        return jsonify({'message': 'Bid genre not found!'}), 404

    bidgenre_data = {
        'id': bidgenre.id,
        'name': bidgenre.name,
        'description': bidgenre.description
    }
    return jsonify({'bidgenre': bidgenre_data})

#Update BidGenre

@app.route('/bidgenre/<bidgenre_id>', methods=['PUT'])
def update_bidgenre(bidgenre_id):
    data = request.get_json()
    bidgenre = BidGenre.query.get(bidgenre_id)
    if not bidgenre:
        return jsonify({'message': 'Bid genre not found!'}), 404

    bidgenre.name = data['name']
    bidgenre.description = data.get('description')

    db.session.commit()
    return jsonify({'message': 'Bid genre updated!'})

#Delete BidGenre

@app.route('/bidgenre/<bidgenre_id>', methods=['DELETE'])
def delete_bidgenre(bidgenre_id):
    bidgenre = BidGenre.query.get(bidgenre_id)
    if not bidgenre:
        return jsonify({'message': 'Bid genre not found!'}), 404

    db.session.delete(bidgenre)
    db.session.commit()
    return jsonify({'message': 'Bid genre deleted!'})

#Controllers
#BidGenre Controller

from flask import Blueprint, render_template, request, redirect, url_for

bidgenre_bp = Blueprint('bidgenre_bp', __name__)

@bidgenre_bp.route('/bidgenres', methods=['GET'])
def bidgenres():
    bidgenres = BidGenre.query.all()
    return render_template('bidgenres.html', bidgenres=bidgenres)

@bidgenre_bp.route('/bidgenre/<bidgenre_id>', methods=['GET'])
def bidgenre(bidgenre_id):
    bidgenre = BidGenre.query.get(bidgenre_id)
    if not bidgenre:
        return render_template('404.html'), 404
    return render_template('bidgenre.html', bidgenre=bidgenre)

@bidgenre_bp.route('/bidgenre/new', methods=['GET', 'POST'])
def new_bidgenre():
    if request.method == 'POST':
        data = request.form
        new_bidgenre = BidGenre(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(new_bidgenre)
        db.session.commit()
        return redirect(url_for('bidgenre_bp.bidgenres'))
    return render_template('new_bidgenre.html')

@bidgenre_bp.route('/bidgenre/edit/<bidgenre_id>', methods=['GET', 'POST'])
def edit_bidgenre(bidgenre_id):
    bidgenre = BidGenre.query.get(bidgenre_id)
    if not bidgenre:
        return render_template('404.html'), 404
    if request.method == 'POST':
        data = request.form
        bidgenre.name = data['name']
        bidgenre.description = data.get('description')
        db.session.commit()
        return redirect(url_for('bidgenre_bp.bidgenres'))
    return render_template('edit_bidgenre.html', bidgenre=bidgenre)

@bidgenre_bp.route('/bidgenre/delete/<bidgenre_id>', methods=['POST'])
def delete_bidgenre(bidgenre_id):
    bidgenre = BidGenre.query.get(bidgenre_id)
    if not bidgenre:
        return render_template('404.html'), 404
    db.session.delete(bidgenre)
    db.session.commit()
    return redirect(url_for('bidgenre_bp.bidgenres'))

#UI Pages with Jinja2 Templates, HTML, and Bootstrap
#bidgenres.html

{% extends "base.html" %}

{% block title %}Bid Genres{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Genres</h1>
    <a href="{{ url_for('bidgenre_bp.new_bidgenre') }}" class="btn btn-primary mb-3">Add New Bid Genre</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bidgenre in bidgenres %}
            <tr>
                <td>{{ bidgenre.id }}</td>
                <td>{{ bidgenre.name }}</td>
                <td>{{ bidgenre.description }}</td>
                <td>
                    <a href="{{ url_for('bidgenre_bp.bidgenre', bidgenre_id=bidgenre.id) }}" class="btn btn-info
btn-sm">View</a
                    <a href="{{ url_for('bidgenre_bp.edit_bidgenre', bidgenre_id=bidgenre.id) }}" class="btn
btn-warning
btn-sm">Edit</a>
                    <form action="{{ url_for('bidgenre_bp.delete_bidgenre', bidgenre_id=bidgenre.id) }}"
method="post"
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#bidgenre.html

{% extends "base.html" %}

{% block title %}Bid Genre Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Genre Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ bidgenre.id }}</td>
        </tr>
        <tr>
            <th>Name</th>
            <td>{{ bidgenre.name }}</td>
        </tr>
        <tr>
            <th>Description</th>
            <td>{{ bidgenre.description }}</td>
        </tr>
    </table>
    <a href="{{ url_for('bidgenre_bp.bidgenres') }}" class="btn btn-secondary">Back to Bid Genres</a>
{% endblock %}

#new_bidgenre.html

{% extends "base.html" %}

{% block title %}New Bid Genre{% endblock %}

{% block content %}
    <h1 class="mt-5">Add New Bid Genre</h1>
    <form action="{{ url_for('bidgenre_bp.new_bidgenre') }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Bid Genre</button>
    </form>
{% endblock %}

#edit_bidgenre.html

{% extends "base.html" %}

{% block title %}Edit Bid Genre{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit Bid Genre</h1>
    <form action="{{ url_for('bidgenre_bp.edit_bidgenre', bidgenre_id=bidgenre.id) }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name" value="{{ bidgenre.name }}" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description">{{ bidgenre.description }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Bid Genre</button>
    </form>
{% endblock %}

#404.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 Not Found</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">404 Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <a href="{{ url_for('bidgenre_bp.bidgenres') }}" class="btn btn-secondary">Back to Bid Genres</a>
    </div>
</body>
</html>

#base.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

#bidgenres.html (using base.html)

{% extends "base.html" %}

{% block title %}Bid Genres{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Genres</h1>
    <a href="{{ url_for('bidgenre_bp.new_bidgenre') }}" class="btn btn-primary mb-3">Add New Bid Genre</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bidgenre in bidgenres %}
            <tr>
                <td>{{ bidgenre.id }}</td>
                <td>{{ bidgenre.name }}</td>
                <td>{{ bidgenre.description }}</td>
                <td>
                    <a href="{{ url_for('bidgenre_bp.bidgenre', bidgenre_id=bidgenre.id) }}" class="btn btn-info
btn-sm">View
                    <a href="{{ url_for('bidgenre_bp.edit_bidgenre', bidgenre_id=bidgenre.id) }}" class="btn
btn-warning
btn-sm">Edit</a>
                    <form action="{{ url_for('bidgenre_bp.delete_bidgenre', bidgenre_id=bidgenre.id) }}"
method="post"
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#bidgenre.html (using base.html)

{% extends "base.html" %}

{% block title %}Bid Genre Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Genre Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ bidgenre.id }}</td>
        </tr>
        <tr>
            <th>Name</th>
            <td>{{ bidgenre.name }}</td>
        </tr>
        <tr>
            <th>Description</th>
            <td>{{ bidgenre.description }}</td>
        </tr>
    </table>
    <a href="{{ url_for('bidgenre_bp.bidgenres') }}" class="btn btn-secondary">Back to Bid Genres</a>
{% endblock %}

#new_bidgenre.html (using base.html)

{% extends "base.html" %}

{% block title %}New Bid Genre{% endblock %}

{% block content %}
    <h1 class="mt-5">Add New Bid Genre</h1>
    <form action="{{ url_for('bidgenre_bp.new_bidgenre') }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Bid Genre</button>
    </form>
{% endblock %}

#edit_bidgenre.html (using base.html)

{% extends "base.html" %}

{% block title %}Edit Bid Genre{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit Bid Genre</h1>
    <form action="{{ url_for('bidgenre_bp.edit_bidgenre', bidgenre_id=bidgenre.id) }}" method="post">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" id="name" name="name" value="{{ bidgenre.name }}" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description">{{ bidgenre.description }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Bid Genre</button>
    </form>
{% endblock %}


