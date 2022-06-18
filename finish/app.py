from flask import Flask, flash, render_template, redirect, url_for, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import sqlite3 
from flask import Flask,render_template,request,redirect,url_for,flash,jsonify,session
from datetime import datetime
from weather import main
import ast
import pickle
import joblib
#####################################################################################
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# print(basedir)
# app.config["SQLALCHEMY_DATABASE_URI"] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

# class Farmer(db.Model):
    # rtc = db.Column(db.String(10))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    
    
########################################################
def predict_production(data):
    fi = open("./ML_model_setup/major_project/pre_pro.pkl","rb")
    combined = pickle.load(fi)
    fi.close()
    print(data)
    print(combined)
    model = joblib.load("/home/amogha/Desktop/amogha_personal/work/random_forest.joblib")
    x = []
    data[0] = combined.index(data[0].upper())+1
    data[1] = int(data[1])
    data[2] = combined.index(data[2])+1
    data[3] = combined.index(data[3])+1
    data[4] = float(data[4])
    res = model.predict([data])
    print(res)
    return res


def fetch_res():
    get_to = datetime.now().strftime("%Y-%m-%d")
    f = open("data_wth.txt","r")
    data = f.read()
    f.close()
    f = 0
    if len(data)!=0:
    	mydi = ast.literal_eval(data)
    if len(data) == 0 :
        main()
        f=1

    elif not mydi.get(get_to,None):
        main()
        f=1

    else:
        return mydi.get(get_to)

    if f==1:
        f= open('data_wth.txt','r')
        data = f.read()
        mydi=ast.literal_eval(data)
        f.close()
        return mydi.get(get_to)

    return []


@app.route('/predict_data',methods=["POST","GET"])
def predict_data():

    if request.method == "POST" :
        # print(request.form.get("em1"))
        print(request.form, len(request.form))
        ans = fetch_res()
        print(ans)
        data = []
        data.append(request.form.get("district"))
        data.append(request.form.get("crop_year"))
        data.append(request.form.get("season"))
        data.append(request.form.get("Crop"))
        data.append(request.form.get("area"))
        data = data + ans
        res = predict_production(data)
        print(res)
        if len(request.form)>5:
            #here add to database all the values of the farmer with rtc number and it will redirect to dashboard for graph
            return redirect(url_for('dashboard',msg="Your value added to production"))
        # print(request.form.get("paswd"))
        flash(f"thanks for submitting !!your value {res} ","success")
        return render_template("predict_data.html",res=res)
    else:
        print("Not enetered",request.method)
        flash("Please fill the feilds","danger")
        return render_template("predict_data.html")

    return render_template("predict_data.html")
    
    
######################################################


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    print("---------------------------------------")
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        try:
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            flash('Username or Email is already in use.','success')
            print("enetrirjng-----------")
            return redirect(url_for('signup'))
            # return render_template('signup.html', exception=e)
        # #     raise e
        #     abort(500)
            

        return render_template('signup_done.html', new_user=new_user)
        # return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@app.route('/dashboard/<msg>')
@login_required
def dashboard(msg=None):
    if msg:
        print(msg)
        flash(f"{msg}","warning")
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
