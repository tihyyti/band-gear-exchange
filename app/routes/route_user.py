# Controller (Routes):
# Define routes for the user-related functionality (e.g., user profile):

# app/user/routes.py
from flask import Blueprint, render_template
from routes import service_db_conn
from routes.service_db_conn import connect_to_db
from routes.service_db_conn import get_user_by_id

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/user_id')
def user_profile(user_id):
    user = get_user_by_id(user_id)
    if user:
        return render_template("view_user.html", user=user)
    else:
        return "User not found", 404

