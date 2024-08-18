
# app.py
from flask import Flask, render_template, request
from models import model_user  # Assuming defined SQLAlchemy models exists if any
import psycopg2

app = Flask(__name__)
app.config["SECRET_KEY"] = ""
app.config["DATABASE_URL"] = "postgresql://postgres:xxxxxxxx@localhost/dbBGEF_v5"

def connect_to_db():
    try:
        conn = psycopg2.connect(app.config["DATABASE_URL"])
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None