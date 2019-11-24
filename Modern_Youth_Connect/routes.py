from flask import render_template, url_for, flash, redirect, request, abort, send_file
from flask_login import login_user, current_user, logout_user, login_required
import os, secrets
from PIL import Image
from Modern_Youth_Connect import app, db, bcrypt
from Modern_Youth_Connect.forms import RegistrationForm, LoginForm, UpdateAccountForm, LoginFormAdmin
from Modern_Youth_Connect.models import User, Admin


@app.route("/")
@app.route("/home", methods=['GET'])
def home():
    # posts=Post.query.all()
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


def save_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)  # underscore throws a variable name
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/files', file_fn)
    file.save(file_path)
    return file_fn


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # and instance of a form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            'utf-8')  # decode converts into bytes
        ssc_file = save_file(form.SSC_marksheet.data)
        hsc_file = save_file(form.HSC_marksheet.data)
        bsc_file = save_file(form.BSC_marksheet.data)
        msc_file = save_file(form.MSC_marksheet.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    firstname=form.firstname.data, lastname=form.lastname.data, bsc_marks=form.BSC_percentage.data,
                    bsc_marksheet=bsc_file, ssc_marks=form.SSC_percentage.data, ssc_marksheet=ssc_file,
                    hsc_marks=form.HSC_percentage.data, hsc_marksheet=hsc_file, msc_marks=form.MSC_percentage.data,
                    msc_marksheet=msc_file)
        db.session.add(user)
        db.session.commit()
        flash('Account created for ' + form.username.data, 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get(
                'next')  # args takes dictonary argument but it will throw error if we use for next so we use ()
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # underscore throws a variable name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # form_picture.save(picture_path)
    output_size = (125, 125)
    resized_new_image = Image.open(form_picture)
    resized_new_image = resized_new_image.resize(output_size)
    resized_new_image.save(picture_path)  # Save the new resized image instead of the actual image
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:  # If user has uploaded image then it will come into this block
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated Successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':  # This will prefill the values already in the form bar
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    form = LoginFormAdmin()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get(
                'next')  # args takes dictonary argument but it will throw error if we use for next so we use ()
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:

            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin-login.html', title='Login', form=form)


@app.route("/admin-dashboard", methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    unverified = User.query.filter_by(verified=False).count()
    verfied = User.query.filter_by(verified=True).count()
    return render_template('admin-dashboard.html', verfied=verfied, unverified=unverified)


@app.route("/view-registered-students", methods=['GET'])
@login_required
def view_all_students():
    student_list = User.query.all()
    return render_template('view-students.html', students=student_list)


@app.route("/view_student")
@login_required
def view_student():
    id = request.args['id']
    form = RegistrationForm()
    student = User.query.filter_by(id=id).first()
    return render_template('view-student.html', form=form, student=student)


@app.route("/view_marksheet")
def view_marksheet():
    file = request.args['file_name']
    file_path = os.path.join(app.root_path, 'static/files', file)
    return send_file(file_path)


@app.route("/verify_student")
@login_required
def verify_student():
    id = request.args['id']
    user = User.query.filter_by(id=id).first()
    user.verify()
    return redirect(url_for('view_student', id=id))
