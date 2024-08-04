
#BidExchange Model

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#BidExchange Model
class BidExchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_id = db.Column(db.Integer, db.ForeignKey('bid_header.id'), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)

#Service Functions
#Create BidExchange

from flask import request, jsonify

@app.route('/bidexchange', methods=['POST'])
def create_bidexchange():
    data = request.get_json()
    new_bidexchange = BidExchange(
        bid_id=data['bid_id'],
        exchange_rate=data['exchange_rate'],
        currency=data['currency'],
        date=data['date']
    )
    db.session.add(new_bidexchange)
    db.session.commit()
    return jsonify({'message': 'New bid exchange created!'}), 201

#Fetch All BidExchanges

@app.route('/bidexchanges', methods=['GET'])
def get_all_bidexchanges():
    bidexchanges = BidExchange.query.all()
    output = []
    for bidexchange in bidexchanges:
        bidexchange_data = {
            'id': bidexchange.id,
            'bid_id': bidexchange.bid_id,
            'exchange_rate': bidexchange.exchange_rate,
            'currency': bidexchange.currency,
            'date': bidexchange.date
        }
        output.append(bidexchange_data)
    return jsonify({'bidexchanges': output})

#Fetch One BidExchange

@app.route('/bidexchange/<bidexchange_id>', methods=['GET'])
def get_one_bidexchange(bidexchange_id):
    bidexchange = BidExchange.query.get(bidexchange_id)
    if not bidexchange:
        return jsonify({'message': 'Bid exchange not found!'}), 404

    bidexchange_data = {
        'id': bidexchange.id,
        'bid_id': bidexchange.bid_id,
        'exchange_rate': bidexchange.exchange_rate,
        'currency': bidexchange.currency,
        'date': bidexchange.date
    }
    return jsonify({'bidexchange': bidexchange_data})

#Update BidExchange

@app.route('/bidexchange/<bidexchange_id>', methods=['PUT'])
def update_bidexchange(bidexchange_id):
    data = request.get_json()
    bidexchange = BidExchange.query.get(bidexchange_id)
    if not bidexchange:
        return jsonify({'message': 'Bid exchange not found!'}), 404

    bidexchange.bid_id = data['bid_id']
    bidexchange.exchange_rate = data['exchange_rate']
    bidexchange.currency = data['currency']
    bidexchange.date = data['date']

    db.session.commit()
    return jsonify({'message': 'Bid exchange updated!'})

#Delete BidExchange

@app.route('/bidexchange/<bidexchange_id>', methods=['DELETE'])
def delete_bidexchange(bidexchange_id):
    bidexchange = BidExchange.query.get(bidexchange_id)
    if not bidexchange:
        return jsonify({'message': 'Bid exchange not found!'}), 404

    db.session.delete(bidexchange)
    db.session.commit()
    return jsonify({'message': 'Bid exchange deleted!'})


#Controller Components
#BidExchange Controller

from flask import Blueprint, render_template, request, redirect, url_for

bidexchange_bp = Blueprint('bidexchange_bp', __name__)

@bidexchange_bp.route('/bidexchanges', methods=['GET'])
def bidexchanges():
    bidexchanges = BidExchange.query.all()
    return render_template('bidexchanges.html', bidexchanges=bidexchanges)

@bidexchange_bp.route('/bidexchange/<bidexchange_id>', methods=['GET'])
def bidexchange(bidexchange_id):
    bidexchange = BidExchange.query.get(bidexchange_id)
    if not bidexchange:
        return render_template('404.html'), 404
    return render_template('bidexchange.html', bidexchange=bidexchange)

@bidexchange_bp.route('/bidexchange/new', methods=['GET', 'POST'])
def new_bidexchange():
    if request.method == 'POST':
        data = request.form
        new_bidexchange = BidExchange(
            bid_id=data['bid_id'],
            exchange_rate=data['exchange_rate'],
            currency=data['currency'],
            date=data['date']
        )
        db.session.add(new_bidexchange)
        db.session.commit()
        return redirect(url_for('bidexchange_bp.bidexchanges'))
    return render_template('new_bidexchange.html')

@bidexchange_bp.route('/bidexchange/edit/<bidexchange_id>', methods=['GET', 'POST'])
def edit_bidexchange(bidexchange_id):
    bidexchange = BidExchange.query.get(bidexchange_id)
    if not bidexchange:
        return render_template('404.html'), 404
    if request.method == 'POST':
        data = request.form
        bidexchange.bid_id = data['bid_id']
        bidexchange.exchange_rate = data['exchange_rate']
        bidexchange.currency = data['currency']
        bidexchange.date = data['date']
        db.session.commit()
        return redirect(url_for('bidexchange_bp.bidexchanges'))
    return render_template('edit_bidexchange.html', bidexchange=bidexchange)

@bidexchange_bp.route('/bidexchange/delete/<bidexchange_id>', methods=['POST'])
def delete_bidexchange(bidexchange_id):
    bidexchange = BidExchange.query.get(bidexchange_id)
    if not bidexchange:
        return render_template('404.html'), 404
    db.session.delete(bidexchange)
    db.session.commit()
    return redirect(url_for('bidexchange_bp.bidexchanges'))

#UI Pages with Jinja2 Templates, HTML, and Bootstrap
#bidexchanges.html

{% extends "base.html" %}

{% block title %}Bid Exchanges{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Exchanges</h1>
    <a href="{{ url_for('bidexchange_bp.new_bidexchange') }}" class="btn btn-primary mb-3">Add New Bid Exchange</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Bid ID</th>
                <th>Exchange Rate</th>
                <th>Currency</th>
                <th>Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bidexchange in bidexchanges %}
            <tr>
                <td>{{ bidexchange.id }}</td>
                <td>{{ bidexchange.bid_id }}</td>
                <td>{{ bidexchange.exchange_rate }}</td>
                <td>{{ bidexchange.currency }}</td>
                <td>{{ bidexchange.date }}</td>
                <td>
                    <a href="{{ url_for('bidexchange_bp.bidexchange', bidexchange_id=bidexchange.id) }}" class="btn btn-info
btn-sm">View</a>
                    <a href="{{ url_for('bidexchange_bp.edit_bidexchange', bidexchange_id=bidexchange.id) }}" class="btn
btn-warning btn-sm">Edit</a>
                    <form action="{{ url_for('bidexchange_bp.delete_bidexchange', bidexchange_id=bidexchange.id) }}" method="post"
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#bidexchange.html

{% extends "base.html" %}

{% block title %}Bid Exchange Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Exchange Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ bidexchange.id }}</td>
        </tr>
        <tr>
            <th>Bid ID</th>
            <td>{{ bidexchange.bid_id }}</td>
        </tr>
        <tr>
            <th>Exchange Rate</th>
            <td>{{ bidexchange.exchange_rate }}</td>
        </tr>
        <tr>
            <th>Currency</th>
            <td>{{ bidexchange.currency }}</td>
        </tr>
        <tr>
            <th>Date</th>
            <td>{{ bidexchange.date }}</td>
        </tr>
    </table>
    <a href="{{ url_for('bidexchange_bp.bidexchanges') }}" class="btn btn-secondary">Back to Bid Exchanges</a>
{% endblock %}

#new_bidexchange.html

{% extends "base.html" %}

{% block title %}New Bid Exchange{% endblock %}

{% block content %}
    <h1 class="mt-5">Add New Bid Exchange</h1>
    <form action="{{ url_for('bidexchange_bp.new_bidexchange') }}" method="post">
        <div class="form-group">
            <label for="bid_id">Bid ID</label>
            <input type="number" class="form-control" id="bid_id" name="bid_id" required>
        </div>
        <div class="form-group">
            <label for="exchange_rate">Exchange Rate</label>
            <input type="number" step="0.01" class="form-control" id="exchange_rate" name="exchange_rate" required>
        </div>
        <div class="form-group">
            <label for="currency">Currency</label>
            <input type="text" class="form-control" id="currency" name="currency" required>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
{% endblock %}


#edit_bidexchange.html

{% extends "base.html" %}

{% block title %}Edit Bid Exchange{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit Bid Exchange</h1>
    <form action="{{ url_for('bidexchange_bp.edit_bidexchange', bidexchange_id=bidexchange.id) }}" method="post">
        <div class="form-group">
            <label for="bid_id">Bid ID</label>
            <input type="number" class="form-control" id="bid_id" name="bid_id" value="{{ bidexchange.bid_id }}" required>
        </div>
        <div class="form-group">
            <label for="exchange_rate">Exchange Rate</label>
            <input type="number" step="0.01" class="form-control" id="exchange_rate" name="exchange_rate" value="{{ bidexchange.
exchange_rate }}" required>
        </div>
        <div class="form-group">
            <label for="currency">Currency</label>
            <input type="text" class="form-control" id="currency" name="currency" value="{{ bidexchange.currency }}" required>
        </div>
        <div class="form-group">
            <label for="date">Date</label>
            <input type="date" class="form-control" id="date" name="date" value="{{ bidexchange.date }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update</button>
    </form>
{% endblock %}

#bidexchanges.html

{% extends "base.html" %}

{% block title %}Bid Exchanges{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Exchanges</h1>
    <a href="{{ url_for('bidexchange_bp.new_bidexchange') }}" class="btn btn-primary mb-3">Add New Bid Exchange</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Bid ID</th>
                <th>Exchange Rate</th>
                <th>Currency</th>
                <th>Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bidexchange in bidexchanges %}
            <tr>
                <td>{{ bidexchange.id }}</td>
                <td>{{ bidexchange.bid_id }}</td>
                <td>{{ bidexchange.exchange_rate }}</td>
                <td>{{ bidexchange.currency }}</td>
                <td>{{ bidexchange.date }}</td>
                <td>
                    <a href="{{ url_for('bidexchange_bp.bidexchange', bidexchange_id=bidexchange.id) }}" class="btn btn-info
btn-sm">View</a>
                    <a href="{{ url_for('bidexchange_bp.edit_bidexchange', bidexchange_id=bidexchange.id) }}" class="btn
btn-warning btn-sm">Edit</a>
                    <form action="{{ url_for('bidexchange_bp.delete_bidexchange', bidexchange_id=bidexchange.id) }}" method="pos
style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

#bidexchange.html

{% extends "base.html" %}

{% block title %}Bid Exchange Details{% endblock %}

{% block content %}
    <h1 class="mt-5">Bid Exchange Details</h1>
    <table class="table table-bordered">
        <tr>
            <th>ID</th>
            <td>{{ bidexchange.id }}</td>
        </tr>
        <tr>
            <th>Bid ID</th>
            <td>{{ bidexchange.bid_id }}</td>
        </tr>
        <tr>
            <th>Exchange Rate</th>
            <td>{{ bidexchange.exchange_rate }}</td>
        </tr>
        <tr>
            <th>Currency</th>
            <td>{{ bidexchange.currency }}</td>
        </tr>
        <tr>
            <th>Date</th>
            <td>{{ bidexchange.date }}</td>
        </tr>
    </table>
    <a href="{{ url_for('bidexchange_bp.bidexchanges') }}" class="btn btn-secondary">Back to Bid Exchanges</a>
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
        <a href="{{ url_for('bidexchange_bp.bidexchanges') }}" class="btn btn-secondary">Back to Bid Exchanges</a>
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

