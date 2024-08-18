
# gear details
@app.route('/gear/<int:gear_id>')
def gear_details(gear_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Gear WHERE id = %s"
        cursor.execute(query, (gear_id,))
        gear = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('gear_details.html', gear=gear)
    else:
        return "Error connecting to the database", 500

if __name__ == "__main__":
    app.run(debug=True)
