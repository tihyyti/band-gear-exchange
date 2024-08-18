# Controller (Routes):
# Define routes for the user-related list all-functionality:

from flask import render_template
from app.models import User

@app.route('/users')
def user_list():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM vw_users"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('user_list.html', users=users)
    else:
        return "Error connecting to the database", 500

if __name__ == "__main__":
    app.run(debug=True)