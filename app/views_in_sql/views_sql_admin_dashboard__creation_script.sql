
# Views for the Admin Dashboard:

# 1. User Summary View:
# This view summarizes user data, including the total number of users, active users, and recent
# sign-ups.

CREATE VIEW vw_user_summary AS
SELECT
    COUNT(*) AS total_users,
    SUM(CASE WHEN last_login >= DATEADD(DAY, -30, GETDATE()) THEN 1 ELSE 0 END) AS active_users,
    SUM(CASE WHEN registration_date >= DATEADD(DAY, -30, GETDATE()) THEN 1 ELSE 0 END) AS
recent_signups
FROM Client;

# 2. Bid Summary View:
# This view groups bids by their status (idle, active, under negotiation, agreed deal, bid ended) and
# sorts them by bidCreatedTime in descending order.

CREATE VIEW vw_bid_summary AS
SELECT
    bidStatus,
    COUNT(*) AS total_bids,
    MAX(bidCreatedTime) AS most_recent_bid
FROM BidHeader
GROUP BY bidStatus;

# 3. Gear Inventory View:
# This view groups gear items by genre (using the vw_gear_by_genre view) and provides information
# about gear availability and maintenance status.

CREATE VIEW vw_gear_inventory AS
SELECT
    genre_name,
    COUNT(*) AS total_gear_items,
    SUM(CASE WHEN gear_availability = 'Available' THEN 1 ELSE 0 END) AS available_items,
    SUM(CASE WHEN gear_maintenance_status = 'Needs Maintenance' THEN 1 ELSE 0 END) AS
items_needing_maintenance
FROM vw_gear_by_genre
GROUP BY genre_name;
