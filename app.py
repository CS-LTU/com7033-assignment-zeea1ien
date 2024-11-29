from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from SQLite_handler import *
import os
import sqlite3
import pymongo
import random as R
import ast
from user import User

create_connection()
app = Flask(__name__)
app.secret_key = "ASecretButNotSoSecretKey"# secret key for secuirty- to protect user session data 
#mongodb = pymongo.MongoClient("mongodb://localhost:27017")

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_fuser(id):
    user_info = user_check_confirmation()
    if len(user_info) <= 0:
        return None
    else:
        return User(user_info[0], user_info[1])
    

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

#Signup
@app.route("/signup")
def signup():
    if current_user.is_authenticated is False:
        return render_template("register.html")
    else:
        return redirect("/")

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    if current_user.is_authenticated is False:
        user_dict = {}
        user_data = request.get_data()
        user_data = user_data.decode()
        user_data = user_data.split("&")
        user_dict["username"] = user_data[0].replace("username=", "")
        user_dict["password"] = user_data[1].replace("password=", "")
        create_user(user_dict)
        return redirect('/')
    else:
        return redirect("/")

# Route to add a new patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    return 'Patient added successfully!'

@app.route('/view_patients')
def view_patients():
    # Retrieve patients from MongoDB
    mongo_patients = list(patient_collection.find())    
    return render_template('patients.html', sqlite_patients=sqlite_patients, mongo_patients=mongo_patients)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
