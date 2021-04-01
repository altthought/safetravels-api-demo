# Author: Alex Culp
# Description: controller for RESTful services and admin panel
# Notes: TODO:
# PUT user (update)

from config import app, db
from datetime import datetime
from flask import abort, jsonify, make_response, Response, render_template
from flask import redirect, url_for, request, session
from forms import Login, AddCompanyForm, AddCouponForm
from models import Company, Coupon, Users, Redeemed
from sqlalchemy.exc import DataError
import json

# HTML response codes (other than 404 ;)
HTML_OK = 200
HTML_OK_CREATED = 201
HTML_ERR_JSON = 400
HTML_ERR_CONFLICT = 409

def logged_in():
    if 'logged_in' not in session:
        session['logged_in'] = False
    return session['logged_in']

# friendly JSON 404 response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

# friendly malformed JSON response (400)
@app.errorhandler(HTML_ERR_JSON)
def malformed_json(error):
    return make_response(jsonify({'error': 'malformed request'}),HTML_ERR_JSON)

# conflict request i.e. attempt to create existing user
@app.errorhandler(HTML_ERR_CONFLICT)
def conflict(error):
    return make_response(jsonify( {'error': 'conflict'}), HTML_ERR_CONFLICT)

# prevent accessing / directory
@app.route('/', strict_slashes = False, methods = ['GET','POST', 'PUT', 'DELETE'])
@app.route('/api', strict_slashes = False, methods = ['GET','POST', 'PUT', 'DELETE'])
def index():
    return abort(404)

# GET/PUT(update) specific user info
@app.route('/api/user/<given_id>', methods = ['GET', 'PUT'])
def get_user(given_id):
    # retrieve user info
    if request.method == 'GET':
        user = Users.query.get(given_id)
        if not user:
            return abort(404)
        return jsonify(user.json_dict())
    # update a user
    elif request.method == 'PUT':
        # quit if JSON lacks needed User fields
        if not all(k in request.json for k in ['user_id','miles_driven', 'pts_earned']):
            return abort(HTML_ERR_JSON)
        user = request.json['user_id']

        # quit if update gives bad integers
        try:
            miles_driven = int(request.json['miles_driven'])
            pts_earned = int(request.json['pts_earned'])
        except (ValueError,TypeError):
            return jsonify({"error": HTML_ERR_JSON})

        # quit if user doesn't already exist
        if not Users.query.get(given_id):
            return abort(404)

        # ready to update
        user = Users.query.get(given_id)
        user.miles_driven = miles_driven
        user.pts_earned = pts_earned
        # writeback to DB 
        db.session.commit()
        return ('',HTML_OK_CREATED)


# GET specific coupon info
@app.route('/api/coupon/<given_id>', methods = ['GET'])
def get_coupon(given_id):
    coupon = Coupon.query.get(given_id)
    if not coupon:
        return abort(404)
    return jsonify(coupon.json_dict())

# GET specific company info
@app.route('/api/company/<given_id>', methods = ['GET'])
def get_company(given_id):
    company = Company.query.get(given_id)
    if not company:
        return abort(404)
    return jsonify(company.json_dict())

# GET info for all companies
@app.route('/api/company', strict_slashes = False, methods = ['GET'])
def get_all_companies():
    companies = Company.query.all()
    # return a JSON array of companies -- using json.dumps because jsonify doesn't like top-level arrays
    return Response(json.dumps([company.json_dict() for company in companies]), mimetype='application/json')
    #return jsonify(results=[company.json_dict() for company in companies])

# GET all coupons for a specific company
@app.route('/api/coupon/by_company/<given_id>', methods = ['GET'])
def get_company_coupons(given_id):
    coupons = Coupon.query.filter_by(company_id = given_id)
    if not coupons:
        return abort(404)
    # return a JSON array of coupons
    return Response(json.dumps([coupon.json_dict() for coupon in coupons]), mimetype='application/json')
    

# POST(add) new user
@app.route('/api/user', methods = ['POST'])
def add_user():
    # make sure the JSON request is correct
    if not request.json or 'user_id' not in request.json:
        return abort(HTML_ERR_JSON) 
    # make sure the user does not already exist
    if not Users.query.get(request.json['user_id']):
        user = Users(request.json['user_id'], 0, 0)
        db.session.add(user)
        db.session.commit()
        return ('', HTML_OK_CREATED)
    # user already exists
    return abort(HTML_ERR_CONFLICT)

# POST(add) new receipt
@app.route('/api/redeemed', methods = ['POST'])
def add_receipt():
    # JSON is not malformed
    if "user_id" in request.json and "coupon_id" in request.json:
        # ensure that coupon_id is an integer
        try:
            int(request.json['coupon_id'])
        except (ValueError,TypeError):
            return jsonify({"error": HTML_ERR_JSON})
        # user does not exist
        if not Users.query.get(request.json['user_id']): 
            return abort(404)
        # coupon does not exist
        if not Coupon.query.get(request.json['coupon_id']):
            return abort(404) 
        # JSON and data are valid
        timestamp = str(datetime.now())
        receipt = Redeemed(request.json['user_id'],request.json['coupon_id'], timestamp)
        # writeback to DB
        db.session.add(receipt)
        db.session.commit()
        return ('', HTML_OK_CREATED) 
    # some other malformed JSON
    else:
        return abort(HTML_ERR_JSON) 


# app routes for management panel
@app.route('/admin', strict_slashes = False, methods = ['GET', 'POST'])
def admin_login():
    error_msg = None
    form = Login(request.form)
    # login attempt
    if request.method == 'POST':
        username = form.username.data.lower()
        password_raw = form.password.data
        
        # ensure fields are non-empty
        if not username or not password_raw:
            error_msg = "Username and password are both required"
            return render_template("login.html", error = error_msg, form = form)
        
        # ensure alphanumeric A-z 0-9 : easiest way to avoid sql/js injection
        if not username.isalnum() or not password_raw.isalnum():
            error_msg = "Invalid username or password"
            return render_template("login.html", error = error_msg, form = form) 
        
        # THESE ARE JUST DUMMY CREDENTIALS FOR TESTING 
        if username == "admin" and password_raw == "password":
            # admin panel goes here
            session['logged_in'] = True
            return redirect(url_for("overview"))
        
        else:
            error_msg = "invalid credentials"
            return render_template("login.html", error = error_msg, form = form) 
    
    elif request.method == 'GET':
        if not logged_in():
            return render_template("login.html", error = error_msg, form = form) 
        return redirect(url_for("overview"))


@app.route('/admin/overview', methods = ['GET', 'POST'])
def overview():
    # clicked logout button
    if request.method == 'POST':
        session['logged_in'] = False
        return redirect(url_for("admin_login"))

    # get the overview page
    elif request.method == 'GET':
        if not logged_in():
            return redirect(url_for("admin_login"))

        # grab last 10 from each table
        c = Company.query.all()[-10:]
        u = Users.query.all()[-10:]
        o = Coupon.query.all()[-10:]
        r = Redeemed.query.all()[-10:]

        return render_template("overview.html", user='admin', companies=c,users=u,coupons=o,redeemed=r)

# add a new company
@app.route('/admin/add_company', methods = ['GET','POST'])
def add_company():
    companyForm = AddCompanyForm(request.form)
    if request.method == 'POST':
        # get raw form data
        name = companyForm.name.data
        street = companyForm.street.data
        city = companyForm.city.data
        state = companyForm.state.data
        image_url = companyForm.image_url.data
        bio = companyForm.bio.data

        address = ",".join([street,city,state])

        new_id = 0
        count = Company.query.count() # doesn't include 0th item
        if count:
            new_id = count + 2 # offset for 0th item 

        # retrieve coordinates from JavaScript API?
        newCompany = Company(new_id, name, address, 0.0, 0.0, bio, image_url)

        # write changes to DB
        db.session.add(newCompany)
        db.session.commit()

        # redirect user back to the main page
        return redirect(url_for("overview"))

    elif request.method == 'GET':
        if not logged_in():
            return redirect(url_for("admin_login"))
        return render_template("add_company.html", form = companyForm)
    

@app.route('/admin/add_coupon', methods = ['GET','POST'])
def add_coupon():
    if not logged_in():
        return redirect(url_for("admin_login"))

    couponForm = AddCouponForm(request.form)

    # THIS NEEDS TYPE CHECKING 
    if request.method == 'POST':

        company_id = couponForm.company_id.data
        pts_required = couponForm.pts_required.data
        summary = couponForm.summary.data
        max_use = couponForm.max_use.data

        # attempt to get numbers or throw error
        try:
            company_id = int(couponForm.company_id.data)
            pts_required = int(couponForm.pts_required.data)
            max_use = int(couponForm.max_use.data)
        except (ValueError, TypeError):
            return jsonify({"error": HTML_ERR_JSON})

        # new_id = 0
        # old_id = Coupon.query.count() # doesn't include 0th item
        # if old_id:
        #     new_id = old_id + 2 # hence + 2 to account for 0 offset
        new_id = Coupon.query.count() + 1
        
        newCoupon = Coupon(new_id, company_id, pts_required, summary, max_use)
        db.session.add(newCoupon)
        db.session.commit()

        # redirect to main overview
        return redirect(url_for("overview"))

    elif request.method == 'GET':
        c = Company.query.all()
        return render_template("add_coupon.html", form = couponForm, companies = c)
