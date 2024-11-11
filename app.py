from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
import pymongo

app = Flask(__name__)
mongodb = pymongo.MongoClient("mongodb://localhost:27017")

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the database
db = SQLAlchemy(app)

# Table 1: User - for user registration
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Password should ideally be hashed

    def __repr__(self):
        return f"<User {self.username}>"

# Table 2: Patient - for patient medical data
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    hypertension = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Patient {self.name}>"

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']  # Password should be hashed for security

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return 'User added successfully!'

# Route to add a new patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    hypertension = bool(request.form.get('hypertension', False))

    new_patient = Patient(name=name, age=age, gender=gender, hypertension=hypertension)
    db.session.add(new_patient)
    db.session.commit()

    return 'Patient added successfully!'

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
