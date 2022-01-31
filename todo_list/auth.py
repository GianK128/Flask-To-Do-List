from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from todo_list.models import User
from todo_list import db

from todo_list.forms import LoginForm, RegisterForm
from todo_list.token import gen_confirm_token, confirm_token
from todo_list.email import send_email

auth = Blueprint('auth', __name__)

@auth.route('signup', methods=['GET', 'POST'])
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
        flash("Se ha registrado exitosamente. Chequee su correo para verificar su cuenta", category='success')
        return redirect(url_for('auth.unconfirmed'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('sign_up.html', form=form)

@auth.route('login', methods=['GET', 'POST'])
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

@auth.route('verify/send-email')
@login_required
def resend_email():
    token = gen_confirm_token(current_user.email)
    url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template(
        'verification/activate_account.html', 
        username=current_user.username,
        confirm_url=url
    )
    send_email(current_user.email, "[To Do List] Confirmación de su cuenta", html)
    return {}

@auth.route('confirm')
@login_required
def confirm_email():
    try:
        email = confirm_token(request.args.get('token'))
    except:
        flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
        return redirect(url_for('routes.home'))
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if user.email_confirmed:
        flash('Esta cuenta ya está confirmada. Por favor ingrese.', 'success')
        return redirect(url_for('auth.login'))
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.commit()
        flash('Esta cuenta ya está confirmada. Por favor ingrese.', 'success')
    return redirect(url_for('routes.home'))

@auth.route('unconfirmed')
@login_required
def unconfirmed():
    if current_user.email_confirmed:
        return redirect(url_for('routes.home'))
    return render_template('verification/unconfirmed_account.html')

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash("Te desconectaste del sitio.", category='info')
    return redirect(url_for('routes.home'))
