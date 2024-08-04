CREATE TABLE User
(
    id SERIAL NOT NULL PRIMARY KEY,
    userName VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(25) DEFAULT NULL,
    email VARCHAR(80) DEFAULT NULL,
    secondaryEmail VARCHAR(80) DEFAULT NULL,
    userIcon_Url VARCHAR(80) DEFAULT NULL,  -- Link to user's user's icon metadata file
    role_id INT NOT NULL,
    blocked BOOLEAN DEFAULT FALSE,
    latestBidHeader_id INT,

    FOREIGN KEY(role_id) REFERENCES Role(id),
    FOREIGN KEY(userIcon_url) REFERENCES ImageMetadata(id),
    FOREIGN KEY(latestBidHeader_id) REFERENCES BidHeader(id)
  );

CREATE TABLE Role
(
    id SERIAL NOT NULL PRIMARY KEY,
    roleName VARCHAR(80) NOT NULL UNIQUE,
    registeredUser BOOLEAN DEFAULT FALSE,
    sellerRole BOOLEAN DEFAULT FALSE,
    buyerRole BOOLEAN DEFAULT FALSE,
    adminRole BOOLEAN DEFAULT FALSE
  );

CREATE TABLE BidGenre
(
    id SERIAL NOT NULL PRIMARY KEY,
    bidGenreHeader VARCHAR(100) NOT NULL UNIQUE,
    user_id INT,
    LastBidHeader_id INT,
    numberOfBids INT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(lastBidHeader_id) REFERENCES  BidHeader(id)
  );

CREATE TABLE BidHeader
(
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INT,
    bidGenre_id INT,
    bidTypeCode INT,
    bidStatus INT,
    bidContent_id INT,
    bidHeaderText VARCHAR(100) NOT NULL UNIQUE,
    bidExchange1_id INT,
    bidExchange2_id INT,
    bidExchange3_id INT,
    bidExchange4_id INT,
    bidExchange5_id INT,
    bidStartedTime TIMESTAMP NOT NULL,
    bidEndingTime TIMESTAMP NOT NULL,
    hdrEditedTime TIMESTAMP NOT NULL,

    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(bidGenre_id) REFERENCES BidGenre(id),
    FOREIGN KEY(bidContent_id) REFERENCES BidContent(id),
    FOREIGN KEY(bidExchange1_id) REFERENCES BidExchange(id),
    FOREIGN KEY(bidExchange2_id) REFERENCES BidExchange(id),
    FOREIGN KEY(bidExchange3_id) REFERENCES BidExchange(id),
    FOREIGN KEY(bidExchange4_id) REFERENCES BidExchange(id),
    FOREIGN KEY(bidExchange5_id) REFERENCES BidExchange(id)
    );


CREATE TABLE BidContent
(
    id SERIAL NOT NULL PRIMARY KEY,
    bidHeader_id INT,
    bidContent VARCHAR(500) NOT NULL,
    gear1_id INT,
    gear2_id INT,
    gear3_id INT,
    gear4_id INT,
    gear5_id INT,
    gear6_id INT,
    gear7_id INT,
    gear8_id INT,
    gear9_id INT,
    gear10_id INT,
    conEditedTime TIMESTAMP NOT NULL,
    bundleImage_id INT, -- Link to bundle image metadata file
    bundleSound_id INT, -- Links to bundle sound sample metadata file

    FOREIGN KEY(bidHeader_id) REFERENCES BidHeader(id),
    FOREIGN KEY(bundleImage_id) REFERENCES ImageMetadata(id),
    FOREIGN KEY(bundleSound_id) REFERENCES SoundClipMetadata(id),
    FOREIGN KEY(gear1_id) REFERENCES Gear(id),
    FOREIGN KEY(gear2_id) REFERENCES Gear(id),
    FOREIGN KEY(gear3_id) REFERENCES Gear(id),
    FOREIGN KEY(gear4_id) REFERENCES Gear(id),
    FOREIGN KEY(gear5_id) REFERENCES Gear(id),
    FOREIGN KEY(gear6_id) REFERENCES Gear(id),
    FOREIGN KEY(gear7_id) REFERENCES Gear(id),
    FOREIGN KEY(gear8_id) REFERENCES Gear(id),
    FOREIGN KEY(gear9_id) REFERENCES Gear(id),
    FOREIGN KEY(gear10_id) REFERENCES Gear(id)
);

CREATE TABLE Gear
(
  id SERIAL NOT NULL PRIMARY KEY,
  gearBrand VARCHAR(30) NOT NULL,
  gearCode INT,
  gearStatus INT,
  bidHeader_id INT,
  gearName VARCHAR(100) NOT NULL,
  gearDetails TEXT,
  gearStory TEXT,
  amountOffered INT NOT NULL,
  approxValue FLOAT default 0.00,
  user_id INT,
  comments TEXT,
  editedTime TIMESTAMP NOT NULL,
  gearImage_id INT,  -- Links to gear image metadata file
  soundClip_id INT, -- Links to gear sound sample metadata file

  FOREIGN KEY(user_id) REFERENCES User(id),
  FOREIGN KEY(bidHeader_id) REFERENCES BidHeader(id),
  FOREIGN KEY(gearImage_id) REFERENCES ImageMetadata(id),
  FOREIGN KEY(soundClip_id) REFERENCES SoundClipMetadata(id)
);

CREATE TABLE BidExchange --This table will allow bidders to exchange equipment based on their bids.
(
    id SERIAL NOT NULL PRIMARY KEY,
    salesBidder_id INT NOT NULL, -- ID of the initial bidder (sales-bidder)
    salesBidHeader_id INT NOT NULL, -- ID of the sales offer header
    purchaseBidder_id INT NOT NULL, -- ID of the bidder making the purchase offer
    purchaseBidHeader_id INT NOT NULL, -- ID of the purchase offer header
    agreedDeal BOOLEAN DEFAULT FALSE, -- Indicates if the deal is mutually agreed upon
    dealTimestamp TIMESTAMP NOT NULL, -- Timestamp when the deal was made

    FOREIGN KEY(salesBidder_id) REFERENCES User(id),
    FOREIGN KEY(salesBidHeader_id) REFERENCES BidHeader(id),
    FOREIGN KEY(purchaseBidder_id) REFERENCES User(id)
    FOREIGN KEY(purchaseBidHeader_id) REFERENCES BidHeader(id),
);

CREATE TABLE ImageMetadata
(
    id SERIAL NOT NULL PRIMARY KEY,
    imageName VARCHAR(100) NOT NULL,
    AxSize VARCHAR(10) NOT NULL,
    resolution VARCHAR(20) NOT NULL,
    image_url VARCHAR(255) NOT NULL -- Link to the actual image file
);

CREATE TABLE SoundClipMetadata
(
    id SERIAL NOT NULL PRIMARY KEY,
    clipName VARCHAR(100) NOT NULL,
    format VARCHAR(10) NOT NULL, -- e.g., '.wav', '.mp3', etc.
    quality VARCHAR(30) NOT NULL, -- e.g., '24-bit WAV', '196 kbps MP3', etc.
    clipLengthInSeconds FLOAT NOT NULL,
    isStereo BOOLEAN NOT NULL,
    sample_url VARCHAR(255) NOT NULL -- Link to the actual sound sample file
);
-- SOME VIEWS FOR TESTING:
CREATE VIEW BidGenreList AS
SELECT bg.id, bg.bidGenreHeader, COUNT(bc.id) as count, MAX(bc.conEditedTime) AS latest
FROM db_bgefv4_schemav2.BidGenre bg
LEFT JOIN db_bgefv4_schemav2.BidHeader bhr ON (bg.id = bhr.bidGenre_id)
LEFT JOIN db_bgefv4_schemav2.BidContent bc ON (bhr.id = bc.bidHeader_id)
GROUP by bg.id, bg.bidGenreHeader;

CREATE VIEW BidList AS
SELECT bh.id, bh.user_id, bh.bidGenre_id, bh. bidTypeCode, bh.bidStatus, bh.bidHeaderText,
COUNT(*) AS count, MIN(bc.coneditedTime) AS edited,
MAX(bc.coneditedTime) AS latest
FROM db_bgefv4_schemav2.BidHeader bh
LEFT JOIN db_bgefv4_schemav2.BidContent bc ON (bh.id = bc.bidHeader_id)
GROUP BY bh.id, bh.bidHeaderText, bh.user_id, bh.bidGenre_id
ORDER BY MAX(bc.coneditedTime) DESC;