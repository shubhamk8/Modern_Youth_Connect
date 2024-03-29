from Modern_Youth_Connect import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg',
                           nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ssc_percentage = db.Column(db.Float)
    ssc_marksheet = db.Column(db.String)
    hsc_percentage = db.Column(db.Float)
    hsc_marksheet = db.Column(db.String)
    bsc_percentage = db.Column(db.Float)
    bsc_marksheet = db.Column(db.String)
    msc_percentage = db.Column(db.Float)
    msc_marksheet = db.Column(db.String)
    cv = db.Column(db.String)
    aggregate = db.Column(db.Float)
    verified = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_students(self):
        return Student.query.all()

    def get_unverified(self):
        return Student.query.filter_by(verfied=False).all()

    def verify(self):
        self.verified = True
        db.session.add(self)
        db.session.commit()

    def calculate_aggregate(self):
        ssc = float(self.ssc_percentage)
        hsc = float(self.hsc_percentage)
        bsc = float(self.bsc_percentage)
        msc = float(self.msc_percentage)
        aggregate = ssc + hsc + bsc + msc
        print(aggregate)
        self.aggregate = aggregate / 4
        db.session.add(self)
        db.session.commit()


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Recruiter(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    company_url = db.Column(db.String)
    job_description = db.relationship("Job_description")


class Job_description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    job_profile = db.Column(db.String)
    skill = db.Column(db.String)
    criteria = db.Column(db.String)
    vacancies = db.Column(db.String)
    recruiter = db.relationship('Recruiter')