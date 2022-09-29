'''Author Vinay Pursnani
This file is the controller file for our flask app
Created on: 09/26/2022
'''

from flask import Flask, render_template, request
# for sending email verification
import smtplib
# for generating security code
import math, random

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# you need to install MYSQL connector
# pip install mysql-connector-python
import mysql.connector
# pip install pymysql
# pip install cryptography

# for password hash
from werkzeug.security import generate_password_hash


myConnection = mysql.connector.connect(
	host="DB.JSTOCKLEY.COM",
	user ="dbadmin",
	password="H4kw3yes!"
	)

c = myConnection.cursor()

myDB = '''SHOW DATABASES'''

c.execute(myDB)

for db in c:
	print(db)



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbadmin:H4kw3yes!@DB.JSTOCKLEY.COM/CS5800 DB'
app.config['SECRET_KEY'] = ""

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

''' weird the function verifyingCredentials is able to access variable 
from login page, envoked by login function'''


@app.route('/email_not_verified')
def emailNotVerified():
	for i in range(10):
		securityCode = digits[math.floor(random.random()*10)]
	
	message = f"Please verify your email with the security sent before login: {securityCode} Once you login with this code this will be permanently associated with your username."
	
	# define the SMTP sever
	# specify which one and the port
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.startls()
	server.login("", "absadsad")
	server.sendemail("gamer2132312ddd@gmail.com", email, message)


	return render_template('verifying_credentials.html')


@app.route('/verifying_credentials', methods=["POST"])
def verifying_credentials():
	email = request.form.get("email") 
	password = request.form.get("password")

	hashedPassword = generate_password_hash(password, method='sha256')

	print(hashedPassword)
	# checking if the user exists

	getEmailPasswordQuery = f"""SELECT password FROM user WHERE email = '{email}'"""
	getEmailPasswordResult = c.execute(getEmailPasswordQuery).fetchone()

	print(getEmailPasswordResult)

	verifiedCheckQuery = f"""SELECT verified_email FROM user WHERE email = '{email}'"""
	verifiedCheckResult = c.execute(verifiedCheckQuery).fetchone()

	print(verifiedCheckResult)

	if hashedPassword == getEmailPasswordResult:
		if verifiedCheck == 1:
			return render_template('verifying_credentials.html', email=email, password=password)
		else:
			return render_template('email_not_verified.html')
	else:
		return render_template('login.html', error_statement=error_statement)

	if not email or not password:
		error_statement = "All Form Fields Required"
		return render_template('login.html', error_statement=error_statement)
