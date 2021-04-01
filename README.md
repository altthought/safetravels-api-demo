SafeTravels Documentation
===================

This is a *DEMO* project containing the outline of the initial API backend for the SafeTravels mobile app. It
also contains a small administrative panel to view and edit API data for testing while demoing the app. 


----------

# **General Notes**
> - All web services are provided by [Flask](http://flask.pocoo.org/), DMBS by [SQLAlchemy](http://www.sqlalchemy.org/)
> - This Flask app is written for **Python 3.4+**, though with some changes can run on Python 2.7+
> - There is no authentication between mobile clients and the web server, though it will be added

## PostgreSQL Database
> **General Notes**
> - Users keeps track of individual rewards earned
> - Company gives information and location 
> - Coupons are *tied to a specific company* and contain specific coupon info
> - Receipts are of the form (User, Coupon) and *cannot be deleted* for security's sake
```
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
  
CREATE TABLE Receipt (
  u_id varchar(64) REFERENCES Users,
  c_id int REFERENCES Coupon,
  PRIMARY KEY (u_id, c_id),
  date_used timestamp NOT NULL
  );
```


### Flask Overall Structure

**```config.py```** --- *Settings for Flask and PostgreSQL/SQLAlchemy*

**```forms.py```** --- *Website forms for adding/editing companies, coupons*

**```models.py```** --- *Database models for Users, Companies, Coupons, Receipts*

**```templates/ ```** --- *Website templates in .html format with placeholders*

**```run.py```** --- *Starts server, controls* ```debug=True```

**```views.py ```** --- *Controller for both RESTful and administrative panel*

### Flask Schema -- RESTful 

#### GET (retrieve) a user
#### POST (create) a user
#### PUT (update) a user
#### DELETE a user

