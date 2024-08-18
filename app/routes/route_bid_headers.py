@app.route('/bid_headers')
def bid_headers_list():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM vw_bid_headers"
        cursor.execute(query)
        bid_headers = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('bid_headers_list.html', bid_headers=bid_headers)
    else:
        return "Error connecting to the database", 500

if __name__ == "__main__":
    app.run(debug=True)