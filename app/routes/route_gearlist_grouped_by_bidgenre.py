
# Gear-list grouped by BidGenre
@app.route('/gear_by_genre')
def gear_by_genre():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM vw_gear_by_genre"
        cursor.execute(query)
        gear_by_genre = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('gear_by_genre.html', gear_by_genre=gear_by_genre)
    else:
        return "Error connecting to the database", 500

if __name__ == "__main__":
    app.run(debug=True)