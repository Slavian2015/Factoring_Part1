from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from app import db
import math, random
import logging

auth = Blueprint('auth', __name__)


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


@auth.route('/login')
def login():
    global otp2


    otp2 = generateOTP()
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    logging.info(otp2)
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    tel = request.form.get('mobile')
    password = request.form.get('password')
    otp_web = request.form.get('otp2')
    remember = True if request.form.get('remember') else False


    user = User.query.filter_by(tel=tel).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    elif otp_web != otp2:
        flash('OTP не совпадают')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/login2')
def login2():
    global otp2
    otp2 = generateOTP()
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    logging.info(otp2)
    return render_template('login2.html')

@auth.route('/login2', methods=['POST'])
def login_post2():
    tel = request.form.get('mobile')
    otp_web = request.form.get('otp2')
    user = User.query.filter_by(tel=tel).first()

    if not user:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login2'))

    elif otp_web != otp2:
        flash('OTP не совпадают')
        return redirect(url_for('auth.login2'))

    login_user(user)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    tel = request.form.get('mobile')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first()

    if user:
        flash('Mobile already exists.')
        return redirect(url_for('auth.signup'))
    if User.query.count() == 0:
        new_user = User(tel=tel, employee=True, name=name, password=generate_password_hash(password, method='sha256'))
    else:
        new_user = User(tel=tel, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/signup2')
def signup2():

    global otp
    otp = generateOTP()
    logging.basicConfig(filename="sample.log", level=logging.INFO)
    logging.info(otp)
    return render_template('signup2.html')

@auth.route('/signup2', methods=['POST'])
def signup_post2():
    tel = request.form.get('mobile')
    name = request.form.get('name')
    password = request.form.get('password')
    password_again = request.form.get('password_again')
    otp_web = request.form.get('otp')
    user = User.query.filter_by(name=name).first()

    if user:
        flash('Mobile already exists.')

        return redirect(url_for('auth.signup2'))
    elif password_again != password:
        flash('Пароли не совпадают')
        return redirect(url_for('auth.signup2'))
    elif otp_web != otp:
        flash('OTP не совпадают')
        return redirect(url_for('auth.signup2'))
    if User.query.count() == 0:
        new_user = User(tel=tel, employee=True, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        new_user = User(tel=tel, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/mobile')
def mobile():
    return render_template('mobile.html')

@auth.route('/mobile', methods=['POST'])
def mobile_post():
    tel = request.form.get('mobile')
    user = User.query.filter_by(tel=tel).first()

    if not user:
        if User.query.all() is None:
            return redirect(url_for('auth.signup2'))  ###  N1
        else:
            return redirect(url_for('auth.signup'))  ###  N2
    else:
        if user.employee == True:
            return redirect(url_for('auth.login'))  ###  N3
        else:
            return redirect(url_for('auth.login2'))  ###  N4