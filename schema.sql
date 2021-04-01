CREATE TABLE Users (
  user_id varchar(64) PRIMARY KEY NOT NULL,
  miles_driven int DEFAULT 0 NOT NULL,
  pts_earned int DEFAULT 0 NOT NULL
  );
  
CREATE TABLE Company (
  company_id int PRIMARY KEY NOT NULL,
  name varchar(128) NOT NULL,
  address varchar(128) NOT NULL,
  latitude double precision,
  longitude double precision,
  bio varchar(512), 
  image_url varchar(128)
  );
  
CREATE TABLE Coupon (
  coupon_id int PRIMARY KEY NOT NULL,
  company_id int REFERENCES Company,
  pts_required int,
  summary varchar(1024),
  max_use int
  );
  
CREATE TABLE Redeemed (
  u_id varchar(64) REFERENCES Users,
  c_id int REFERENCES Coupon,
  PRIMARY KEY (u_id, c_id),
  date_used timestamp NOT NULL
  );
