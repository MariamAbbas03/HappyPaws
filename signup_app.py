from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask('__name__')
app.secret_key = 'your-secret-key'

import os

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


#MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ' '
app.config['MYSQL_DB'] = 'flask_users'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'HappyPaws@gmail.com'
app.config['MAIL_PASSWORD'] = 'HappyPaws123'

mysql = MySQL(app)
mail = Mail(app)

# Regular expression pattern for validating email addresses
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')

def send_confirmation_email(email, username):
    msg = Message('Signup Confirmation', recipients=[email])
    msg.body = f'Dear {username},\n\nThank you for signing up at Happy Paws!!'
    mail.send(msg)

@app.route('/signup/customer', methods=['GET','POST'])
def SignUpCustomer():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        pwd = request.form['password']

        # Check if the email address is valid
        if not EMAIL_REGEX.match(email):
            error = "Please enter a valid email address."
        else:
            # Send confirmation email to the user
            send_confirmation_email(email, username)
            cur = mysql.connection.cursor()
            cur.execute(f"insert into tbl_users (username, email, password) values ('{username}','{email}', '{pwd}')")
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('home'))
    return render_template('signup.html', error=error)


@app.route('/signup/petshop', methods=['GET','POST'])
def SignUpPetshop():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        document = request.files['document']
        # Check if the email address is valid
        if not EMAIL_REGEX.match(email):
            error = "Please enter a valid email address."
        # Check if the uploaded file is a PDF
        elif document.filename == '' or not document.filename.endswith('.pdf'):
            error = "Please upload a PDF file."
        else:
            # Send confirmation email to the user
            send_confirmation_email(email, username)
            cur = mysql.connection.cursor()
            cur.execute(f"insert into tbl_users (username, email, password) values ('{username}','{email}', '{password}')")
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('home'))
    return render_template('signuppetshop.html',error=error)


@app.route('/signup/shelter', methods=['GET','POST'])
def SignUpShelter():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        document = request.files['document']
        # Check if the email address is valid
        if not EMAIL_REGEX.match(email):
            error = "Please enter a valid email address."
        # Check if the uploaded file is a PDF
        elif document.filename == '' or not document.filename.endswith('.pdf'):
            error = "Please upload a PDF file."
        else:
            # Send confirmation email to the user
            send_confirmation_email(email, username)
            cur = mysql.connection.cursor()
            cur.execute(f"insert into tbl_users (username, email, password) values ('{username}','{email}', '{password}')")
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('home'))
    return render_template('signupshelter.html', error=error)   


