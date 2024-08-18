
# Main Python Module (run.py)
# The main Python module to run the Flask app:Python

from flask import Flask
#from config import DATABASE_URL

from routes.home_bp import home_bp
from routes.route_user import user_bp
from routes.route_gear_details import gear_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = ""
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:xxxxx@localhost/dbBGEF_v5"

app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(user_bp, url_prefix="/user/user_id")
app.register_blueprint(gear_bp, url_prefix="/gear/gear_id")

if __name__ == "__main__":
    app.run(debug=True)