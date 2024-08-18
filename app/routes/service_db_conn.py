# Service (Database Connectivity):
# database connectivity using psycopg2 (PostgreSQL adapter) and basic SQL queries:

# app/service.py
import psycopg2
#from run import DATABASE_URL

# app.config["SECRET_KEY"] = "0b6a3f3205bd3b63b803d815c938a981"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postinLent0@localhost/dbBGEF_v5"

def connect_to_db():
    try:
        conn = psycopg2.connect("postgresql://postgres:postinLent0@localhost/dbBGEF_v5")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_user_by_id(user_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        int_user_id = int(user_id)
        query = "SELECT * FROM client WHERE id = %s"
        cursor.execute(query, (int_user_id,))
        #cursor.execute(query, int_user_id)
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return user_data
    return None