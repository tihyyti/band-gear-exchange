
from flask import Blueprint, render_template
from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')