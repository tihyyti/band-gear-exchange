
-- Create a SQL View (vw_gear_by_genre) that groups gear items by BidGenre
CREATE VIEW vw_gear_by_genre AS
SELECT
    g.id AS gear_id,
    g.gearname,
    g.gearbrand,
    bg.bidgenreheadertext
FROM Gear g
JOIN BidGenre bg ON g.bidgenre_id = bg.id
GROUP BY g.id, g.gearname, g.gearbrand, bg.bidgenreheadertext;