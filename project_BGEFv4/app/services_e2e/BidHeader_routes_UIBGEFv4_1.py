#BidHeader Model
class BidHeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

#Service Functions
#Create BidHeader

from flask import request, jsonify

@app.route('/bidheader', methods=['POST'])
def create_bidheader():
    data = request.get_json()
    new_bidheader = BidHeader(
        title=data['title'],
        description=data.get('description'),
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_bidheader)
    db.session.commit()
    return jsonify({'message': 'New bid header created!'}), 201

#Fetch All BidHeaders

@app.route('/bidheaders', methods=['GET'])
def get_all_bidheaders():
    bidheaders = BidHeader.query.all()
    output = []
    for bidheader in bidheaders:
        bidheader_data = {
            'id': bidheader.id,
            'title': bidheader.title,
            'description': bidheader.description,
            'start_date': bidheader.start_date,
            'end_date': bidheader.end_date
        }
        output.append(bidheader_data)
    return jsonify({'bidheaders': output})

#Fetch One BidHeader

@app.route('/bidheader/<bidheader_id>', methods=['GET'])
def get_one_bidheader(bidheader_id):
    bidheader = BidHeader.query.get(bidheader_id)
    if not bidheader:
        return jsonify({'message': 'Bid header not found!'}), 404

    bidheader_data = {
        'id': bidheader.id,
        'title': bidheader.title,
        'description': bidheader.description,
        'start_date': bidheader.start_date,
        'end_date': bidheader.end_date
    }
    return jsonify({'bidheader': bidheader_data})

#Update BidHeader

@app.route('/bidheader/<bidheader_id>', methods=['PUT'])
def update_bidheader(bidheader_id):
    data = request.get_json()
    bidheader = BidHeader.query.get(bidheader_id)
    if not bidheader:
        return jsonify({'message': 'Bid header not found!'}), 404

    bidheader.title = data['title']
    bidheader.description = data.get('description')
    bidheader.start_date = data['start_date']
    bidheader.end_date = data['end_date']

    db.session.commit()
    return jsonify({'message': 'Bid header updated!'})

#Delete BidHeader

@app.route('/bidheader/<bidheader_id>', methods=['DELETE'])
def delete_bidheader(bidheader_id):
    bidheader = BidHeader.query.get(bidheader_id)
    if not bidheader:
        return jsonify({'message': 'Bid header not found!'}), 404

    db.session.delete(bidheader)
    db.session.commit()
    return jsonify({'message': 'Bid header deleted!'})

#Flask Controller Components
#BidHeader Controller

from flask import Blueprint, render_template, request, redirect, url_for

bidheader_bp = Blueprint('bidheader_bp', __name__)

@bidheader_bp.route('/bidheaders', methods=['GET'])
def bidheaders():
    bidheaders = BidHeader.query.all()
    return render_template('bidheaders.html', bidheaders=bidheaders)

@bidheader_bp.route('/bidheader/<bidheader_id>', methods=['GET'])
def bidheader(bidheader_id):
    bidheader = BidHeader.query.get(bidheader_id)
    if not bidheader:
        return render_template('404.html'), 404
    return render_template('bidheader.html', bidheader=bidheader)

@bidheader_bp.route('/bidheader/new', methods=['GET', 'POST'])
def new_bidheader():
    if request.method == 'POST':
        data = request.form
        new_bidheader = BidHeader(
            title=data['title'],
            description=data.get('description'),
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        db.session.add(new_bidheader)
        db.session.commit()
        return redirect(url_for('bidheader_bp.bidheaders'))
    return render_template('new_bidheader.html')

@bidheader_bp.route('/bidheader/edit/<bidheader_id>', methods=['GET', 'POST'])
def edit_bidheader(bidheader_id):
    bidheader = BidHeader.query.get(bidheader_id)
    if not bidheader:
        return render_template('404.html'), 404
    if request.method == 'POST':
        data = request.form
        bidheader.title = data['title']
        bidheader.description = data.get('description')
        bidheader.start_date = data['start_date']
        bidheader.end_date = data['end_date']
        db.session.commit()
        return redirect(url_for('bidheader_bp.bidheaders'))
    return render_template('edit_bidheader.html', bidheader=bidheader)

@bidheader_bp.route('/bidheader/delete/<bidheader_id>', methods=['POST'])
def delete_bidheader(bidheader_id):
    bidheader = BidHeader.query.get(bidheader_id)
    if not bidheader:
        return render_template('404.html'), 404
    db.session.delete(bidheader)
    db.session.commit()
    return redirect(url_for('bidheader_bp.bidheaders'))

#UI Pages with Jinja2 Templates, HTML, and Bootstrap
#bidheaders.html

{% extends "base.html" %}

{% block title %}Bid Headers{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Headers</h1>
    <a href="{{ url_for('bidheader_bp.new_bidheader') }}" class="btn btn-primary mb-3">Add New Bid Heade
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bidheader in bidheaders %}
            <tr>
                <td>{{ bidheader.id }}</td>
                <td>{{ bidheader.title }}</td>
                <td>{{ bidheader.description }}</td>
                <td>{{ bidheader.start_date }}</td>
                <td>{{ bidheader.end_date }}</td>
                <td>
                    <a href="{{ url_for('bidheader_bp.bidheader', bidheader_id=bidheader.id) }}" class="
a>
                    <a href="{{ url_for('bidheader_bp.edit_bidheader', bidheader_id=bidheader.id) }}" cl
btn-sm">Edit</a>
                    <form action="{{ url_for('bidheader_bp.delete_bidheader', bidheader_id=bidheader.id)
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#bidheader.html

{% extends "base.html" %}

{% block title %}Bid Header Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Header Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ bidheader.id }}</td>
        </tr>
        <tr>
            <th>Title</th>
            <td>{{ bidheader.title }}</td>
        </tr>
        <tr>
            <th>Description</th>
            <td>{{ bidheader.description }}</td>
        </tr>
        <tr>
            <th>Start Date</th>
            <td>{{ bidheader.start_date }}</td>
        </tr>
        <tr>
            <th>End Date</th>
            <td>{{ bidheader.end_date }}</td>
        </tr>
    </table>
    <a href="{{ url_for('bidheader_bp.bidheaders') }}" class="btn btn-secondary">Back to Bid Headers</a>
{% endblock %}

#new_bidheader.html

{% extends "base.html" %}

{% block title %}New Bid Header{% endblock %}

{% block content %}
    <h1 class="mt-5">Add New Bid Header</h1>
    <form action="{{ url_for('bidheader_bp.new_bidheader') }}" method="post">
        <div class="form-group">
            <label for="title">Title</label>
            <input type="text" class="form-control" id="title" name="title" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description"></textarea>
        </div>
        <div class="form-group">
            <label for="start_date">Start Date</label>
            <input type="date" class="form-control" id="start_date" name="start_date" required>
        </div>
        <div class="form-group">
            <label for="end_date">End Date</label>
            <input type="date" class="form-control" id="end_date" name="end_date" required>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
{% endblock %}

#edit Bidheader

{% extends "base.html" %}

{% block title %}Edit Bid Header{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit Bid Header</h1>
    <form action="{{ url_for('bidheader_bp.edit_bidheader', bidheader_id=bidheader.id) }}" method="post">
        <div class="form-group">
            <label for="title">Title</label>
            <input type="text" class="form-control" id="title" name="title" value="{{ bidheader.title }}" required>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" name="description">{{ bidheader.description }}</textarea>
        </div>
        <div class="form-group">
            <label for="start_date">Start Date</label>
            <input type="date" class="form-control" id="start_date" name="start_date" value="{{ bidheader.start_date }}"
        </div>
        <div class="form-group">
            <label for="end_date">End Date</label>
            <input type="date" class="form-control" id="end_date" name="end_date" value="{{ bidheader.end_date }}" requir
        </div>
        <button type="submit" class="btn btn-primary">Update Bid Header</button>
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
        <a href="{{ url_for('bidheader_bp.bidheaders') }}" class="btn btn-secondary">Back to Bid Headers</a>
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
