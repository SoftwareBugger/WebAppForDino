from app import db, app, UPLOAD_FOLDER, review, brand, item, review, reviewer, login_manager
import os
from forms import ReviewForm, BrandForm, ItemReviewForm, RegistrationForm, LoginForm
import imageio as iio
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

admin_email = ['hlyu42@wisc.edu']

# user loader that loads user into memory
@login_manager.user_loader
def load_user(user_id):
  return reviewer.query.get(int(user_id))

@app.route('/', methods = ["GET", "POST"])
def index():
    curr_brand = brand.query.all()
    return render_template('main_page.html', brand = curr_brand)

# user route
@app.route('/user/<username>')
@login_required
def user(username):
  user = reviewer.query.filter_by(username=username).first_or_404()
  curr_brand = brand.query.all()
  return render_template('user.html', user=user, brand = curr_brand)

@app.route('/admin/<username>', methods = ["GET","POST"])
def admin(username):
    user = reviewer.query.filter(reviewer.username == username).first_or_404()
    if user.email in admin_email:
        return render_template('admin.html', username = username, form = BrandForm())
    else:
       flash('Sorry, only administrators can have access to this page')
       return redirect(url_for('user', username = username, _external=True, _scheme='http'))

@app.route('/<brand_name>/<username>/usermode', methods = ["GET", "POST"])
@login_required
def brands(brand_name, username):
    this_brand = brand.query.filter(brand.name == brand_name).first_or_404()
    items = item.query.filter(item.brand_id == this_brand.id).all()
    user = reviewer.query.filter(reviewer.username == username).first_or_404()
    return render_template("brands.html", Brand = this_brand, item_list = items, user = user, form = ReviewForm())

@app.route('/<brand_name>', methods = ["GET", "POST"])
def brands_browse(brand_name):
    this_brand = brand.query.filter(brand.name == brand_name).first_or_404()
    items = item.query.filter(item.brand_id == this_brand.id).all()
    return render_template("brands.html", Brand = this_brand, item_list = items, user = None, form = ReviewForm())

@app.route('/<brand_name>/<item_name>/<username>', methods = ["GET", "POST"])
@login_required
def items(brand_name, item_name, username):
    this_brand = brand.query.filter(brand.name == brand_name).first_or_404()
    this_item = item.query.filter(item.name == item_name).first_or_404()
    all_reviews = review.query.filter(review.item_id == this_item.id).all()
    user = reviewer.query.filter(reviewer.username == username).first_or_404()
    return render_template("reviews_on_items.html", Brand = this_brand, review_list = all_reviews, Item = this_item, user = user, form = ItemReviewForm())

@app.route('/<brand_name>/<item_name>', methods = ["GET", "POST"])
def items_browse(brand_name, item_name):
    this_brand = brand.query.filter(brand.name == brand_name).first_or_404()
    this_item = item.query.filter(item.name == item_name).first_or_404()
    all_reviews = review.query.filter(review.item_id == this_item.id).all()
    return render_template("reviews_on_items.html", Brand = this_brand, review_list = all_reviews, Item = this_item, user = None, form = ItemReviewForm())

@app.route('/add_review/<curr_brand_id>/<username>', methods = ["GET","POST"])
@login_required
def add_review(curr_brand_id, username):
    ## Validate and collect the form data
    form = ReviewForm(csrf_enabled = False)
    if form.validate_on_submit():
        item_name = form.name.data
        user_id = reviewer.query.filter(reviewer.username == username).first_or_404().id
        Rating = form.rating.data
        Description = form.description.data
        file = form.file.data.read()
        file_path = UPLOAD_FOLDER + '/' + form.file.data.filename
        if os.path.exists(file_path):
            print('file already exists')
        else:
            # create a file
            fp = open(file_path, 'wb')
            # uncomment if you want empty file
            fp.write(file)
            fp.close()
            fp = iio.imread(file_path)
            # save the file !! I have been desperately searching this step for years!!!
        new_item = item(name = item_name, brand_id = curr_brand_id, icon = file_path)
        db.session.add(new_item)
        db.session.commit()
        new_review = review(image = file_path, description = Description, rating = Rating, item_id = new_item.id, reviewer_id = user_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("brands", brand_id = curr_brand_id, username = username, brand_name = brand.query.get(curr_brand_id).name, _external = True, _scheme = 'http'))
    else:
        # for now, the scheme can only be http
        return redirect(url_for("index", _external = True, _scheme = 'http'))
    ## Redirect to brands route function

@app.route('/add_brand/<username>', methods = ["GET","POST"])
def adminPage(username):
    form = BrandForm(csrf_enabled = False)
    if form.validate_on_submit():
        Name = form.name.data
        Description = form.description.data
        file = form.file.data.read()
        file_path = UPLOAD_FOLDER + '/' + form.file.data.filename
        if os.path.exists(file_path):
            print('file already exists')
        else:
            # create a file
            fp = open(file_path, 'wb')
            # uncomment if you want empty file
            fp.write(file)
            fp.close()
            fp = iio.imread(file_path)
            # save the file !! I have been desperately searching this step for years!!!
        newBrand = brand(name = Name, image = file_path, description = Description, items = item.query.all())
        newBrand.items = item.query.filter(item.brand_id == newBrand.id)
        db.session.add(newBrand)
        db.session.commit()
    return redirect(url_for("user", username = username, _external = True, _scheme = 'http'))

@app.route('/add_review_on_item/<curr_item_id>/<username>', methods = ["GET","POST"])
@login_required
def add_review_on_item(curr_item_id, username):
    ## Validate and collect the form data
    form = ItemReviewForm(csrf_enabled = False)
    if form.validate_on_submit():
        user = reviewer.query.filter(reviewer.username == username).first_or_404()
        user_id = user.id
        Rating = form.rating.data
        Description = form.description.data
        file = form.file.data.read()
        file_path = UPLOAD_FOLDER + '/' + form.file.data.filename
        if os.path.exists(file_path):
            print('file already exists')
        else:
            # create a file
            fp = open(file_path, 'wb')
            # uncomment if you want empty file
            fp.write(file)
            fp.close()
            fp = iio.imread(file_path)
            # save the file !! I have been desperately searching this step for years!!!
        new_review = review(image = file_path, description = Description, rating = Rating, item_id = curr_item_id, reviewer_id = user_id)
        db.session.add(new_review)
        db.session.commit()
        this_brand = brand.query.get(item.query.get(curr_item_id).brand_id)
        return render_template("reviews_on_items.html", Brand = this_brand, review_list = review.query.filter(review.item_id == curr_item_id).all(), Item = item.query.get(curr_item_id), form = ItemReviewForm(), user = user)
    else:
        # for now, the scheme can only be http
        return redirect(url_for("index", _external = True, _scheme = 'https'))
    ## Redirect to brands route function

# registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(csrf_enabled=False)
  if form.validate_on_submit():
    user = reviewer(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    try:
       db.session.add(user)
       user.isAdministrator = False
       db.session.commit()
       login_user(user)
       return redirect(url_for('user', username = user.username, _external=True, _scheme='https'))
    except:
       flash("This email or username has been used, please use a new one")
       return render_template('register.html', title='Register', form=form)
  return render_template('register.html', title='Register', form=form)  

@app.route('/login', methods=['GET','POST'])
@login_manager.unauthorized_handler
def login():
  form = LoginForm(csrf_enabled=False)
  if form.validate_on_submit():
    user = reviewer.query.filter_by(email=form.email.data).first()
    if user and user.check_password(form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('user', username = user.username, _external=True, _scheme='https'))
    else:
      flash("Username unfound or incorrect password")
      return redirect(url_for('login', _external=True, _scheme='https'))
  elif form.is_submitted():
     flash("Input format incorrect, please enter email and password")
  return render_template('login.html', form=form)

@app.route("/delete<username>/<review_id>")
def delete(review_id, username):
  review_deleted = review.query.get(review_id)
  image = review_deleted.image
  image_needed = False
  for singgle_review in review.query.all():
    if singgle_review != review_deleted and singgle_review.image == image:
            image_needed = True
            break
  if not image_needed:
    for single_brand in brand.query.all():
      if single_brand.image == image:
        image_needed = True
        break
  if not image_needed:
    for single_item in item.query.all():
      if single_item.icon == image:
        image_needed = True
        break
      
  if not image_needed:
    os.remove(image)
  db.session.delete(review_deleted)
  db.session.commit()
  return redirect(url_for('profile', username = username))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/profile/<username>")
@login_required
def profile(username):
   user = reviewer.query.filter(reviewer.username == username).first_or_404()
   all_reviews = review.query.filter(review.reviewer_id == user.id).all()
   return render_template('profile.html', user = user, all_reviews = all_reviews)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login', _external=True, _scheme='https'))

