from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import secrets
import os
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

AVATAR_FOLDER = 'static/images/avatars/'

# ---Avatar upload---

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('static/images/avatars', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('name')
        last_name = request.form.get('snamee')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        file = request.files['avatar']
        

        # avatar_url = url_for('static', filename='images/avatars/' + current_user.avatar)



        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. ' + avatar, category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:

            new_user = User(email=email, first_name=first_name, last_name=last_name, avatar=file.filename, 
                    password=generate_password_hash(password1, method='sha256'))
            

            db.session.add(new_user)
            db.session.commit()

            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('website/static/images/avatars/', filename))
                
                # flash("Succesfully  registered!" + request.form.get('firstname'))

                # return redirect(url_for('views.home', name=filename))

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

