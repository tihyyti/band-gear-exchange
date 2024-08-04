--Sample Test Data for db_BGEFv4

--role Table
INSERT INTO db_bgefv4_schemav2.role (id, rolename, registereduser, sellerrole, buyerrole, adminrole)
VALUES
    (1,'Admin', true, false, false, true),
    (2,'Seller', true, true, false, false),
    (3,'Buyer', true, false, true, false);

--client Table
INSERT INTO db_bgefv4_schemav2.client (id, username, password, email, secondaryemail, usericon_url, role_id, blocked, latestbidheader_id)
VALUES
    (1,'user1', 'password1', 'user1@example.com', 'user1_secondary@example.com', 'http://example.com/icon1.png', 1, false, NULL),
    (2,'user2', 'password2', 'user2@example.com', 'user2_secondary@example.com', 'http://example.com/icon2.png', 2, false, NULL);

--bidgenre Table
INSERT INTO db_bgefv4_schemav2.bidgenre (id, bidgenreheader, user_id, lastbidheader_id, numberofbids)
VALUES
    (1, 'Genre 1', 1, NULL, 1),
    (2, 'Genre 2', 2, NULL, 3);

--bidheader Table
INSERT INTO db_bgefv4_schemav2.bidheader (id, user_id, bidgenre_id, bidtypecode, bidstatus, bidcontent_id, bidheadertext, bidexchange1_id, bidexchange2_id, bidexchange3_id, bidexchange4_id, bidexchange5_id, bidstartedtime, bidendingtime, hdreditedtime)
VALUES
    (1, 1, 1, 1, 1, NULL, 'Header Text 1', NULL, NULL, NULL, NULL, NULL, '2024-08-04 00:00:00', '2024-08-05 00:00:00', '2024-08-04 00:00:00'),
    (2, 2, 2, 3, 2, NULL, 'Header Text 2', NULL, NULL, NULL, NULL, NULL, '2024-08-04 01:00:00', '2024-08-05 01:00:00', '2024-08-04 01:00:00');

--bidcontent Table
INSERT INTO db_bgefv4_schemav2.bidcontent (id, bidheader_id, bidcontent, gear1_id, gear2_id, gear3_id, gear4_id, gear5_id, gear6_id, gear7_id, gear8_id, gear9_id, gear10_id, coneditedtime, bundleimage_id, bundlesound_id)
VALUES
    (1, 1, 'Sample content 1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-08-04 00:00:00', NULL, NULL),
    (2, 2, 'Sample content 2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2024-08-04 01:00:00', NULL, NULL);

--bidexchange Table
INSERT INTO db_bgefv4_schemav2.bidexchange (id, salesbidder_id, salesbidheader_id, purchasebidder_id, purchasebidheader_id, agreeddeal, dealtimestamp)
VALUES
    (1, 1, 1, 2, 2, false, '2024-08-04 02:00:00'),
    (2, 2, 2, 1, 1, true, '2024-08-04 03:00:00');

--gear Table
INSERT INTO db_bgefv4_schemav2.gear (id, gearbrand, gearcode, gearstatus, bidheader_id, gearname, geardetails, gearstory, amountoffered,approxvalue, user_id, comments, editedtime, gearimage_id, soundclip_id)
VALUES
    (1, 'Brand A', 1001, 1, 1, 'Gear Name 1', 'Details about gear 1', 'Story about gear 1', 10, 100.00, 1, 'No comments', '2024-08-04 00:00:00', NULL, NULL),
    (2, 'Brand B', 1002, 2, 2, 'Gear Name 2', 'Details about gear 2', 'Story about gear 2', 20, 200.00, 2, 'No comments', '2024-08-04 01:00:00', NULL, NULL);

--imagemetadata Table
INSERT INTO db_bgefv4_schemav2.imagemetadata (id, imagename, axsize, resolution, image_url)
VALUES
    (1, 'Image 1', '1024x768', '300dpi', 'http://example.com/image1.png'),
    (2, 'Image 2', '800x600', '200dpi', 'http://example.com/image2.png');

--soundclipmetadata Table
INSERT INTO db_bgefv4_schemav2.soundclipmetadata (id, clipname, format, quality, cliplengthinseconds, isstereo, sample_url)
VALUES
    (1, 'Clip 1', 'mp3', 'high', 120.5, true, 'http://example.com/clip1.mp3'),
    (2, 'Clip 2', 'wav', 'medium', 240.0, false, 'http://example.com/clip2.wav');