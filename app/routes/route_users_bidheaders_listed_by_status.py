
# User's BidHeaders listed and grouped based on BidHeader status
@app.route('/user_bids_by_bidstatus')
def user_bids_by_bidstatus():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM vw_user_bids_by_bidstatus"
        cursor.execute(query)
        user_bids_by_bidstatus = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('user_bids_by_bidstatus.html',
user_bids_by_bidstatus=user_bids_by_bidstatus)
    else:
        return "Error connecting to the database", 500

if __name__ == "__main__":
    app.run(debug=True)