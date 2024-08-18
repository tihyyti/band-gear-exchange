
# Route BidHeader details
@app.route('/bid_header/<int:bid_id>')
def bid_header_details(bid_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM BidHeader WHERE id = %s"
        cursor.execute(query, (bid_id,))
        bid_header = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('bid_header_details.html', bid_header=bid_header)
    else:
        return "Error connecting to the database", 500

if __name__ == "__main__":
    app.run(debug=True)