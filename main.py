from flask import Flask,render_template,request,redirect,session,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import os.path
import json
from flask_mail import Mail

with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=True

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir,"ff.db")

db = SQLAlchemy(app)
app.secret_key = "mysecretkey"

UPLOAD_FOLDER = 'static/uploads'
ppic='static/profilepics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_1'] = 'static/ppic'

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail=Mail(app)

class contact_vii(db.Model):
    sid=db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Phone = db.Column(db.Integer, nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    Subject = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=True)
    Email = db.Column(db.String(20), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(100), nullable=False, default="profile.jpg")
    phone = db.Column(db.Integer, nullable=False)

class Packages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120),nullable=False)
    rating = db.Column(db.Float, nullable=False)
    dprice = db.Column(db.Integer, nullable=False)
    oprice = db.Column(db.Integer, nullable=False)



@app.route("/book/<int:id>")
def book(id):
    if "username" not in session:
        return redirect('/login')
    package=Packages.query.filter_by(id=id).first()
    return render_template('city.html',p=package)

@app.route("/")
def index():
    packages=Packages.query.all()
    if "username" in session:
        new = User.query.filter_by(username=session["username"]).first()
        return render_template('index.html',params=params,packages=packages,user=new)
    return render_template('index.html',params=params,packages=packages)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if(request.method=='POST'):
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('passw1')
        password2 = request.form.get('passw2')
        if password1!=password2:
            return render_template("signup.html",q='Password mismatch,please retype password')
        if User.query.filter(User.username == username).first():
            return render_template("signup.html",q='username is already exists,Please try another username')
        entry = User(username=username,email = email ,password=password1)
        db.session.add(entry)
        db.session.commit()
        session["username"] = username
        return redirect('/')
    return render_template('signup.html')
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('passw')
        if User.query.filter(User.username == username and User.password==password).first():
            session["username"] = username
            return redirect('/')
        else:
            return render_template("login.html",q='username or password is incorrect')
    return render_template('login.html')

@app.route('/profile/<string:user>', methods=["GET", "POST"])
def profile(user):
    if "username" not in session:
        return redirect('/login')
    new = User.query.filter_by(username=user).first()
    if request.method == "POST":
        new.password = request.form["pass"]
        new.email = request.form["email"]
        new.phone = request.form["phone"]
        image=request.files['ppic']
        if image:
            imagename=new.username +'.jpg'
            new.image=imagename
            save_path = os.path.join(app.config['UPLOAD_FOLDER_1'] , imagename)
            if os.path.exists(save_path):
                os.remove(save_path)
            image.save(save_path)
        db.session.commit()
        return redirect('/profile/'+new.username)
    return render_template('profile.html',user=new)

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect('/')

@app.route('/Adminlogin', methods=["GET", "POST"])
def adminlog():
    if request.method == "POST":
        usern = request.form["username"]
        upass = request.form["pass"]
        if(usern=='nils' and upass=='nil123'):
            session["ausername"] = usern
            return redirect('/admin/addpackage')
        else:
            return render_template('adminlogin.html',q='username or password is incorrect')
    return render_template('adminlogin.html')

@app.route("/admin/addpackage", methods = ['GET', 'POST'])
def addpackage():
    if "ausername" not in session:
        return redirect('/Adminlogin')
    if(request.method=='POST'):
        name = request.form.get('name')
        description = request.form.get('description')
        rating = request.form.get('rating')
        dprice = request.form.get('dprice')
        oprice = request.form.get('oprice')
        image = request.files['image']
        filename = image.filename
        if Packages.query.filter(Packages.name == name,Packages.description == description,Packages.rating == rating,Packages.dprice == dprice,Packages.oprice == oprice).first():
            return render_template('addpackage.html',usern=session["username"],q='This Package is already added.')
        existing_cities = Packages.query.filter_by(image=filename).all()
        if existing_cities:
            # if it exists, add a number to the filename
            count = 1
            while True:
                new_filename = f"{os.path.splitext(filename)[0]} ({count}){os.path.splitext(filename)[1]}"
                existing_cities = Packages.query.filter_by(image=new_filename).all()
                if existing_cities:
                    count += 1
                else:
                    filename = new_filename
                    break
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        entry = Packages(image=filename,name=name, description = description, rating=rating,dprice = dprice ,oprice=oprice)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    return render_template('addpackage.html',usern=session["username"])

@app.route("/edit/package/<int:id>", methods=["GET", "POST"])
def editpackage(id):
    if "ausername" not in session:
        return redirect('/Adminlogin')
    s = Packages.query.filter_by(id=id).first()
    if request.method == "POST":
        s.name = request.form.get('name')
        s.description = request.form.get('description')
        s.rating = request.form.get('rating')
        s.dprice = request.form.get('dprice')
        s.oprice = request.form.get('oprice')
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], s.filename))
        db.session.commit()
        return redirect('/adminindex')
    return render_template('addpackage.html',usern=session["username"],Package=s)
@app.route("/kk", methods = ['GET', 'POST'])
def hell():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        subject = request.form.get('subject')
        entry = contact_vii(Name=name, Phone = phone, Message=message, Date= datetime.now(),Email = email ,Subject=subject)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New query from ' + name,sender=email,recipients = [params['gmail-user']],body = message + "\n" + phone)
        mail.send_message(name + ' Sir, Your query submiited' ,sender=email,recipients = [email], body = message + "\n" + phone)
        return render_template('kk.html',params=params, redirect_time=4)
    time.sleep(4)
    return render_template('index.html',params=params)
# @app.route("/login")
# def about():
#     return render_template('login.html',params=params)


@app.route("/payment/<int:id>")
def paym(id):
    if "username" not in session:
        return redirect('/login')
    package=Packages.query.filter_by(id=id).first()
    return render_template('payment.html',p=package)
app.run(debug=True)