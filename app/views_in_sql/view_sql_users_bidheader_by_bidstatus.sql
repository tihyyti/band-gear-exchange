-- Create a SQL View (vw_user_bids_by_bidstatus) that groups BidHeaders by bidStatus
CREATE VIEW vw_user_bids_by_bidstatus AS
SELECT
    bh.id AS bid_id,
    bh.bidHeaderText,
    bh.bidStatus,
    bh.bidStartingTime,
    bh.bidEndingTime
FROM BidHeader bh
JOIN Client c ON bh.user_id = c.id
WHERE c.userName = 'emilyd' -- Replace with the actual username
ORDER BY bh.bidStatus, bh.hdrCreatedTime DESC;