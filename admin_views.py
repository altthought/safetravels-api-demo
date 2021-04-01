
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
        new_id = Coupon.query.count()
        
        newCoupon = Coupon(new_id, company_id, pts_required, summary, max_use)
        db.session.add(newCoupon)
        db.session.commit()

        # redirect to main overview
        return redirect(url_for("overview"))

    elif request.method == 'GET':
        c = Company.query.all()
        return render_template("add_coupon.html", form = couponForm, companies = c)
