
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

CREATE TABLE Client
(
    id SERIAL NOT NULL PRIMARY KEY,
    userName VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(25) DEFAULT NULL,
    email VARCHAR(50) DEFAULT NULL,
    secondaryEmail VARCHAR(50) DEFAULT NULL,
    userIcon_id INT DEFAULT NULL,  -- Link to user's user's icon metadata file
    roleName VARCHAR(50) NOT NULL UNIQUE,
    registeredUser BOOLEAN DEFAULT FALSE,
    sellerRole BOOLEAN DEFAULT FALSE,
    buyerRole BOOLEAN DEFAULT FALSE,
    adminRole BOOLEAN DEFAULT FALSE,
    blocked BOOLEAN DEFAULT FALSE

    FOREIGN KEY(userIcon_id) REFERENCES ImageMetadata(id)
  );

CREATE TABLE BidGenre
(
    id SERIAL NOT NULL PRIMARY KEY,
    bidGenreHeader VARCHAR(100) NOT NULL UNIQUE
  );

CREATE TABLE BidExchange --This table will allow bidders to exchange equipment based on their bids.
(
    id SERIAL NOT NULL PRIMARY KEY,
    salesBidder_id INT NOT NULL, -- ID of the initial bidder (sales-bidder)
    salesBidHeader_id INT NOT NULL, -- ID of the sales offer header
    purchaseBidder_id INT NOT NULL, -- ID of the bidder making the purchase offer
    purchaseBidHeader_id INT NOT NULL, -- ID of the purchase offer header
    agreedDeal BOOLEAN DEFAULT FALSE, -- Indicates if the deal is mutually agreed upon
	otherConditions TEXT, -- Other conditions of the deal, which are mutually agreed upon
	addOnValue FLOAT default 0.00, -- monetary compensation part of the agreed deal
    dealTimestamp TIMESTAMP NOT NULL, -- Timestamp when the deal was made

    FOREIGN KEY(salesBidder_id) REFERENCES Client(id),
    FOREIGN KEY(salesBidHeader_id) REFERENCES BidHeader(id),
    FOREIGN KEY(purchaseBidder_id) REFERENCES Client(id),
    FOREIGN KEY(purchaseBidHeader_id) REFERENCES BidHeader(id)
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
  createdTime TIMESTAMP NOT NULL,
  editedTime TIMESTAMP NOT NULL,
  gearImage_id INT,  -- Links to gear image metadata file
  soundClip_id INT, -- Links to gear sound sample metadata file

  FOREIGN KEY(user_id) REFERENCES Client(id),
  FOREIGN KEY(bidHeader_id) REFERENCES BidHeader(id)
  FOREIGN KEY(gearImage_id) REFERENCES ImageMetadata(id),
  FOREIGN KEY(soundClip_id) REFERENCES SoundClipMetadata(id)
);

CREATE TABLE BidHeader
(
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INT,
    bidGenre_id INT,
    bidTypeCode INT,
    bidStatus INT,
	bidexchange_id INT,
    bidHeaderText VARCHAR(100) NOT NULL UNIQUE,
    bidContent VARCHAR(300) NOT NULL,
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
    bundleImage_id INT, -- Link to bundle image metadata file
    bundleSound_id INT, -- Links to bundle sound sample metadata file
	hdrEditedTime TIMESTAMP NOT NULL,
	conEditedTime TIMESTAMP NOT NULL,
    bidStartingTime TIMESTAMP NOT NULL,
    bidEndingTime TIMESTAMP NOT NULL,
	bidCreatedTime TIMESTAMP NOT NULL,

    FOREIGN KEY(user_id) REFERENCES Client(id),
    FOREIGN KEY(bidGenre_id) REFERENCES BidGenre(id),
    FOREIGN KEY(bundleImage_id) REFERENCES ImageMetadata(id),
    FOREIGN KEY(bundleSound_id) REFERENCES SoundClipMetadata(id),
	FOREIGN KEY(bidexchange_id) REFERENCES BidExchange(id)
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
