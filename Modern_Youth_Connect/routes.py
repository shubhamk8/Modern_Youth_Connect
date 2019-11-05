from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
import os,secrets
from PIL import Image
from Modern_Youth_Connect import app, db, bcrypt
from Modern_Youth_Connect.forms import RegistrationForm, LoginForm, UpdateAccountForm,PostForm
from Modern_Youth_Connect.models import User


@app.route("/")
@app.route("/home",methods=['GET'])
def home():
    # posts=Post.query.all()
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # and instance of a form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            'utf-8')  # decode converts into bytes
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, firstname=form.firstname.data, lastname=form.lastname.data, bsc_marks=form.BSC_marks.data, ssc_marks=form.SSC_marks.data, hsc_marks=form.HSC_marks.data, msc_marks=form.MSC_marks.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {form.username.data}', 'success')
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
    _, f_ext = os.path.splitext(form_picture.filename)#underscore throws a variable name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #form_picture.save(picture_path)
    output_size = (125, 125)
    resized_new_image = Image.open(form_picture)
    resized_new_image=Image.thumbnail(output_size)
    resized_new_image.save(picture_path)# Save the new resized image instead of the actual image
    return picture_fn


@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:#If user has uploaded image then it will come into this block
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated Successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':#This will prefill the values already in the form bar
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


# @app.route("/post/new", methods=['GET','POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post=Post(title=form.title.data, content=form.content.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your Post has been created','success')
#         return redirect(url_for('home'))
#     return  render_template('create_post.html',title='New Post',form=form,legend='New Post')
#
# @app.route("/post/<int:post_id>")
# @login_required
# def post(post_id):
#     post=Post.query.get_or_404(post_id)#to get something by ID we can use the get method.
#     return render_template('post.html',title=post.title,post=post)
#
# @app.route("/post/<int:post_id>/update",methods=['GET','POST'])
# @login_required
# def update_post(post_id):
#     post=Post.query.get_or_404(post_id)
#     if post.author!=current_user:
#         abort(403)
#     form=PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html',title=post.title, form=form, legend='Update Post')

