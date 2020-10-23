from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from flask_login import login_user
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask import Markup

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 

@auth.route('/signup',methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if(email == '' or name == '' or password == ''):
            flash('Please enter all the fields.')
            return redirect(url_for('auth.signup'))
    user = User.query.filter_by(email=email).first() 

    if(user): 
        flash(Markup('Email address already exists. Please go to <a href="http://127.0.0.1:5000/login" class="alert-link">Login Page</a>'))
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()   
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('profile'))


@auth.route('/account_set')
@login_required
def account_set():
	return render_template('settings.html')

@auth.route('/set1', methods=["GET", "POST"])
@login_required
def set1():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('setting1.html')
    else:
        new_email = request.form.get('email')
        if(new_email == ''):
            flash('Email field is left blank.')
            return redirect(url_for('auth.set1'))

        user = User.query.get_or_404(current_user.id)
        user.email = new_email
        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.set1'))
        flash('Successfully Updated!')
        return redirect(url_for('auth.set1'))

@auth.route('/set2', methods=["GET", "POST"])
@login_required
def set2():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('setting2.html')
    else:
        new_psw = request.form.get('password')
        con_psw = request.form.get('confirmpass')
        if(new_psw == '' or con_psw == ''):
            flash('Password field is left blank.')
            return redirect(url_for('auth.set2'))
        if(new_psw != con_psw):
            flash('Passwords do not match')
            return redirect(url_for('auth.set2'))
        passhash = generate_password_hash(new_psw, method='sha256')
        user = User.query.get_or_404(current_user.id)
        user.password = passhash
        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.set2'))
        flash('Successfully Updated!')
        return redirect(url_for('auth.set2'))


@auth.route('/cancel account')
def cancel():
    from app import current_user
    if current_user is None:
        return redirect(url_for('index'))
    try:
        db.session.delete(current_user)
        db.session.commit()
    except:
        return 'unable to delete the user.'
    flash('Your account has been deleted')
    return redirect(url_for('auth.login'))



