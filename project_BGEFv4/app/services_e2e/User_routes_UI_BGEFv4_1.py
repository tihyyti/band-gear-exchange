
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

db = SQLAlchemy()

#User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

#Service Functions
#Create User

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'}), 201

#Fetch All Users

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        }
        output.append(user_data)
    return jsonify({'users': output})

#Fetch One User

@app.route('/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password
    }
    return jsonify({'user': user_data})

#Update User

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    user.username = data['username']
    user.email = data['email']
    user.password = data['password']

    db.session.commit()
    return jsonify({'message': 'User updated!'})

#Delete User

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'})


#User Controller

from flask import Blueprint, render_template, request, redirect, url_for

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@user_bp.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template('404.html'), 404
    return render_template('user.html', user=user)

@user_bp.route('/user/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        data = request.form
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_bp.users'))
    return render_template('new_user.html')

@user_bp.route('/user/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template('404.html'), 404
    if request.method == 'POST':
        data = request.form
        user.username = data['username']
        user.email = data['email']
        user.password = data['password']
        db.session.commit()
        return redirect(url_for('user_bp.users'))
    return render_template('edit_user.html', user=user)

@user_bp.route('/user/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template('404.html'), 404
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_bp.users'))

# UI Pages with Jinja2 Templates, HTML, and Bootstrap
# users.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Users</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Users</h1>
        <a href="{{ url_for('user_bp.new_user') }}" class="btn btn-primary mb-3">Add New User</a>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                        <a href="{{ url_for('user_bp.user', user_id=user.id) }}" class="btn btn-info btn-sm">View</a
                        <a href="{{ url_for('user_bp.edit_user', user_id=user.id) }}" class="btn btn-warning
btn-sm">Edit</
                        <form action="{{ url_for('user_bp.delete_user', user_id=user.id) }}" method="post"
style="display:i
                            <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>

#user.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Details</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">User Details</h1>
        <table class="table table-bordered">
            <tr>
                <th>ID</th>
                <td>{{ user.id }}</td>
            </tr>
            <tr>
                <th>Username</th>
                <td>{{ user.username }}</td>
            </tr>
            <tr>
                <th>Email</th>
                <td>{{ user.email }}</td>
            </tr>
        </table>
        <a href="{{ url_for('user_bp.users') }}" class="btn btn-secondary">Back to Users</a>
    </div>
</body>
</html>

#new_user.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New User</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Add New User</h1>
        <form action="{{ url_for('user_bp.new_user') }}" method="post">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Add User</button>
        </form>
    </div>
</body>
</html>

#edit_user.html

{% extends "base.html" %}

{% block title %}Edit User{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit User</h1>
    <form action="{{ url_for('user_bp.edit_user', user_id=user.id) }}" method="post">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="{{ user.username }}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" value="{{ user.password }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update User</button>
    </form>
{% endblock %}

{% extends "base.html" %}

{% block title %}Edit User{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit User</h1>
    <form action="{{ url_for('user_bp.edit_user', user_id=user.id) }}" method="post">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="{{ user.username }}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" value="{{ user.password }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update User</button>
    </form>
{% endblock %}

{% extends "base.html" %}

{% block title %}Edit User{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit User</h1>
    <form action="{{ url_for('user_bp.edit_user', user_id=user.id) }}" method="post">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="{{ user.username }}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" value="{{ user.password }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update User</button>
    </form>
{% endblock %}

{% extends "base.html" %}

{% block title %}Edit User{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit User</h1>
    <form action="{{ url_for('user_bp.edit_user', user_id=user.id) }}" method="post">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="{{ user.username }}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" value="{{ user.password }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update User</button>
    </form>
{% endblock %}

{% extends "base.html" %}

{% block title %}Edit User{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit User</h1>
    <form action="{{ url_for('user_bp.edit_user', user_id=user.id) }}" method="post">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="{{ user.username }}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" value="{{ user.password }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update User</button>
    </form>
{% endblock %}

{% extends "base.html" %}

{% block title %}Edit User{% endblock %}

{% block content %}
    <h1 class="mt-5">Edit User</h1>
    <form action="{{ url_for('user_bp.edit_user', user_id=user.id) }}" method="post">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" value="{{ user.username }}" required>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" name="email" value="{{ user.email }}" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" value="{{ user.password }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update User</button>
    </form>
{% endblock %


