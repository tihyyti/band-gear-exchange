-- Create a SQL View (vw_bid_headers) with essential content from BidHeader
CREATE VIEW vw_bid_headers AS
SELECT
    id,
    bidHeaderText,
    bidContentText,
    bidStartingTime,
    bidEndingTime
FROM BidHeader;