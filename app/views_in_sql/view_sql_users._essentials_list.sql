-- Create a SQL View (vw_users) that includes essential user data
CREATE VIEW vw_users AS
SELECT
    id,
    userName,
    email,
    roleName,
    blocked
FROM Client;