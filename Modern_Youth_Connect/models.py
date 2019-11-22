from Modern_Youth_Connect import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg',
                           nullable=False)  # we hash the image file so we need to specify the string size
    password = db.Column(db.String(60), nullable=False)
    ssc_marks = db.Column(db.Float)
    ssc_marksheet = db.Column(db.String)
    hsc_marks = db.Column(db.Float)
    hsc_marksheet = db.Column(db.String)
    bsc_marks = db.Column(db.Float)
    bsc_marksheet = db.Column(db.String)
    msc_marks = db.Column(db.Float)
    msc_marksheet = db.Column(db.String)

    def get_student(self):
        return User.query.all()


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

