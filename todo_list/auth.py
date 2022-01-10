from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from todo_list.models import User
from todo_list import db

from todo_list.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Se ha registrado exitosamente.", category='success')
        return redirect(url_for('list.my_lists', user=new_user.username))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('sign_up.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        
        if attempted_user and attempted_user.check_password_correct(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"¡Hola {attempted_user.username}!", category='success')
            return redirect(url_for('list.my_lists', user=attempted_user.username))
        else:
            flash("El usuario o la contraseña son incorrectos.", category='danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash("Te desconectaste del sitio.", category='info')
    return redirect(url_for('routes.home'))
