# Author: Alex Culp
# Description: models.py -- database models 
# Notes: '_sa_instance_state' is an unneeded SQLAlchemy variable

from config import db
from config import MAX_USERNAME, MAX_CONTACT_INFO, MAX_BIO, MAX_SUMMARY

class Users(db.Model):
    user_id = db.Column(db.String(MAX_USERNAME), primary_key = True)
    miles_driven = db.Column(db.Integer)
    pts_earned = db.Column(db.Integer)
    
    def __init__(self, u_id, miles, points):
        self.user_id = u_id
        self.miles_driven = miles
        self.pts_earned = points

    def __str__(self):
        return "id: {}, miles: {}, pts: {}".format(self.user_id,self.miles_driven,self.pts_earned)
    
    def json_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if k != '_sa_instance_state'}

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(MAX_CONTACT_INFO))
    address = db.Column(db.String(MAX_CONTACT_INFO))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    bio = db.Column(db.String(MAX_BIO))
    image_url = db.Column(db.String(MAX_CONTACT_INFO))  
    
    def __init__(self, c_id, name, addr, lat, lng, bio, img_url):
        self.company_id = c_id
        self.name = name
        self.address = addr
        self.latitude = lat
        self.longitude = lng
        self.bio = bio
        self.image_url = img_url 

    def __str__(self):
        return "id: {}, name: {}, addr: {}, lat: {}, lng: {}, bio: {}, url: {}".format(self.company_id,self.name, self.address,self.latitude,self.longitude,self.bio,self.image_url)

    def json_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if k != '_sa_instance_state'} 

class Coupon(db.Model):
    coupon_id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
    pts_required = db.Column(db.Integer)
    summary = db.Column(db.String(MAX_SUMMARY))
    max_use = db.Column(db.Integer)
    
    def __init__(self, coupon, company, pts, summary, use):
        self.coupon_id = coupon
        self.company_id = company
        self.pts_required = pts
        self.summary = summary
        self.max_use = use

    def __str__(self):
        return "coupon: {}, company: {}, pts_req: {}, summary: {}, max_use: {}".format(self.coupon_id,self.company_id,self.pts_required,self.summary,self.max_use)

    def json_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if k != '_sa_instance_state'}

class Redeemed(db.Model):
    u_id = db.Column(db.String(MAX_USERNAME), db.ForeignKey('users.user_id'), primary_key = True)
    c_id = db.Column(db.Integer, db.ForeignKey('coupon.coupon_id'), primary_key = True) 
    date_used = db.Column(db.DateTime(timezone = False))
    
    def __init__(self, user, coupon, date):
        self.u_id = user
        self.c_id = coupon
        self.date_used = date

    def __str__(self):
        return "user: {}, coupon: {}, date_used: {}".format(self.u_id,self.c_id,self.date_used)

    def json_dict(self):
        return {k: self.__dict__[k] for k in self.__dict__ if k != '_sa_instance_state'}

