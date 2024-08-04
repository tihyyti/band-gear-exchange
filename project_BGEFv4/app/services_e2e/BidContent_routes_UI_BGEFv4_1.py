
#BidContent Model

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#BidContent Model
class BidContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header_id = db.Column(db.Integer, db.ForeignKey('bid_header.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

#Service Functions
#Create BidContent

from flask import request, jsonify

@app.route('/bidcontent', methods=['POST'])
def create_bidcontent():
    data = request.get_json()
    new_bidcontent = BidContent(
        header_id=data['header_id'],
        content=data['content']
    )
    db.session.add(new_bidcontent)
    db.session.commit()
    return jsonify({'message': 'New bid content created!'}), 201

#Fetch All BidContents

@app.route('/bidcontents', methods=['GET'])
def get_all_bidcontents():
    bidcontents = BidContent.query.all()
    output = []
    for bidcontent in bidcontents:
        bidcontent_data = {
            'id': bidcontent.id,
            'header_id': bidcontent.header_id,
            'content': bidcontent.content,
            'created_at': bidcontent.created_at,
            'updated_at': bidcontent.updated_at
        }
        output.append(bidcontent_data)
    return jsonify({'bidcontents': output})

#Fetch One BidContent

@app.route('/bidcontent/<bidcontent_id>', methods=['GET'])
def get_one_bidcontent(bidcontent_id):
    bidcontent = BidContent.query.get(bidcontent_id)
    if not bidcontent:
        return jsonify({'message': 'Bid content not found!'}), 404

    bidcontent_data = {
        'id': bidcontent.id,
        'header_id': bidcontent.header_id,
        'content': bidcontent.content,
        'created_at': bidcontent.created_at,
        'updated_at': bidcontent.updated_at
    }
    return jsonify({'bidcontent': bidcontent_data})

#Update BidContent

@app.route('/bidcontent/<bidcontent_id>', methods=['PUT'])
def update_bidcontent(bidcontent_id):
    data = request.get_json()
    bidcontent = BidContent.query.get(bidcontent_id)
    if not bidcontent:
        return jsonify({'message': 'Bid content not found!'}), 404

    bidcontent.header_id = data['header_id']
    bidcontent.content = data['content']

    db.session.commit()
    return jsonify({'message': 'Bid content updated!'})

#Delete BidContent

@app.route('/bidcontent/<bidcontent_id>', methods=['DELETE'])
def delete_bidcontent(bidcontent_id):
    bidcontent = BidContent.query.get(bidcontent_id)
    if not bidcontent:
        return jsonify({'message': 'Bid content not found!'}), 404

    db.session.delete(bidcontent)
    db.session.commit()
    return jsonify({'message': 'Bid content deleted!'})


#Controller Components
#BidContent Controller

from flask import Blueprint, render_template, request, redirect, url_for

bidcontent_bp = Blueprint('bidcontent_bp', __name__)

@bidcontent_bp.route('/bidcontents', methods=['GET'])
def bidcontents():
    bidcontents = BidContent.query.all()
    return render_template('bidcontents.html', bidcontents=bidcontents)

@bidcontent_bp.route('/bidcontent/<bidcontent_id>', methods=['GET'])
def bidcontent(bidcontent_id):
    bidcontent = BidContent.query.get(bidcontent_id)
    if not bidcontent:
        return render_template('404.html'), 404
    return render_template('bidcontent.html', bidcontent=bidcontent)

@bidcontent_bp.route('/bidcontent/new', methods=['GET', 'POST'])
def new_bidcontent():
    if request.method == 'POST':
        data = request.form
        new_bidcontent = BidContent(
            header_id=data['header_id'],
            content=data['content']
        )
        db.session.add(new_bidcontent)
        db.session.commit()
        return redirect(url_for('bidcontent_bp.bidcontents'))
    return render_template('new_bidcontent.html')

@bidcontent_bp.route('/bidcontent/edit/<bidcontent_id>', methods=['GET', 'POST'])
def edit_bidcontent(bidcontent_id):
    bidcontent = BidContent.query.get(bidcontent_id)
    if not bidcontent:
        return render_template('404.html'), 404
    if request.method == 'POST':
        data = request.form
        bidcontent.header_id = data['header_id']
        bidcontent.content = data['content']
        db.session.commit()
        return redirect(url_for('bidcontent_bp.bidcontents'))
    return render_template('edit_bidcontent.html', bidcontent=bidcontent)

@bidcontent_bp.route('/bidcontent/delete/<bidcontent_id>', methods=['POST'])
def delete_bidcontent(bidcontent_id):
    bidcontent = BidContent.query.get(bidcontent_id)
    if not bidcontent:
        return render_template('404.html'), 404
    db.session.delete(bidcontent)
    db.session.commit()
    return redirect(url_for('bidcontent_bp.bidcontents'))

#UI Pages with Jinja2 Templates, HTML, and Bootstrap
#bidcontents.html

{% extends "base.html" %}

{% block title %}Bid Contents{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Contents</h1>
    <a href="{{ url_for('bidcontent_bp.new_bidcontent') }}" class="btn btn-primary mb-3">Add New Bid Content</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Header ID</th>
                <th>Content</th>
                <th>Created At</th>
                <th>Updated At</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bidcontent in bidcontents %}
            <tr>
                <td>{{ bidcontent.id }}</td>
                <td>{{ bidcontent.header_id }}</td>
                <td>{{ bidcontent.content }}</td>
                <td>{{ bidcontent.created_at }}</td>
                <td>{{ bidcontent.updated_at }}</td>
                <td>
                    <a href="{{ url_for('bidcontent_bp.bidcontent', bidcontent_id=bidcontent.id) }}" class="btn btn-info
btn-sm">View</a>
                    <a href="{{ url_for('bidcontent_bp.edit_bidcontent', bidcontent_id=bidcontent.id) }}" class="btn btn-warning
btn-sm">Edit</a>
                    <form action="{{ url_for('bidcontent_bp.delete_bidcontent', bidcontent_id=bidcontent.id) }}" method="post"
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#bidcontent.html

{% extends "base.html" %}

{% block title %}Bid Content Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Content Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ bidcontent.id }}</td>
        </tr>
        <tr>
            <th>Header ID</th>
            <td>{{ bidcontent.header_id }}</td>
        </tr>
        <tr>
            <th>Content</th>
            <td>{{ bidcontent.content }}</td>
        </tr>
        <tr>
            <th>Created At</th>
            <td>{{ bidcontent.created_at }}</td>
        </tr>
        <tr>
            <th>Updated At</th>
            <td>{{ bidcontent.updated_at }}</td>
        </tr>
    </table>
    <a href="{{ url_for('bidcontent_bp.bidcontents') }}" class="btn btn-secondary">Back to Bid Contents</a>
{% endblock %}

#new_bidcontent.html

{% extends "base.html" %}

{% block title %}New Bid Content{% endblock %}

{% block content %}
    <h1 class="mt-5">Add New Bid Content</h1>
    <form action="{{ url_for('bidcontent_bp.new_bidcontent') }}" method="post">
        <div class="form-group">
            <label for="header_id">Header ID</label>
            <input type="number" class="form-control" id="header_id" name="header_id" required>
        </div>
        <div class="form-group">
            <label for="content">Content</label>
            <textarea class="form-control" id="content" name="content" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Bid Content</button>
    </form>
{% endblock %}

#edit_bidcontent.htm

{% extends "base.html" %}

{% block title %}Edit Bid Content{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit Bid Content</h1>
    <form action="{{ url_for('bidcontent_bp.edit_bidcontent', bidcontent_id=bidcontent.id) }}" method="post">
        <div class="form-group">
            <label for="header_id">Header ID</label>
            <input type="number" class="form-control" id="header_id" name="header_id" value="{{ bidcontent.header_id }}" required>
        </div>
        <div class="form-group">
            <label for="content">Content</label>
            <textarea class="form-control" id="content" name="content" required>{{ bidcontent.content }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Bid Content</button>
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
        <a href="{{ url_for('bidcontent_bp.bidcontents') }}" class="btn btn-secondary">Back to Bid Contents</a>
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
