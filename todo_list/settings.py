import email
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from todo_list import db
from todo_list.token import gen_confirm_token, confirm_token
from todo_list.email import send_email
from todo_list.forms import ChangePasswordForm, ChangeEmailForm, ForgotPasswordForm, ResetPasswordForm
from todo_list.models import User

settings = Blueprint('settings', __name__)

def send_confirmation_email_anon(url_endpoint, html_to_send, email_subject, email_address, url_fallback):
    user = User.query.filter_by(email=email_address).first()
    if user:
        html = render_template(
            html_to_send, 
            username=user.username,
            confirm_url=url_endpoint
        )
        send_email(user.email, email_subject, html)
        return True
    else:
        flash("No hay un usuario registrado con ese nombre")
        return redirect(url_fallback)

def send_confirmation_email(url_endpoint, html_to_send, email_subject):
    html = render_template(
        html_to_send, 
        username=current_user.username,
        confirm_url=url_endpoint
    )
    send_email(current_user.email, email_subject, html)

@settings.route('/', methods=['GET', 'POST'])
@login_required
def main():
    password_form = ChangePasswordForm()
    email_form = ChangeEmailForm()

    if password_form.validate_on_submit():
        if current_user.check_password_correct(attempted_password=password_form.old_password.data):
            password_token = gen_confirm_token(password_form.new_password.data)
            user_token = gen_confirm_token(current_user.username)
            send_confirmation_email(
                url_endpoint = url_for('settings.change_password', token = password_token, u = user_token, _external = True),
                html_to_send = 'verification/change_password.html',
                email_subject = '[To Do List] Cambio de contraseña'
            )
            current_user.active_token = password_token
            db.session.commit()
            return redirect(url_for('settings.main', openModal='password_mail'))
        else:
            flash('La contraseña que ingresó es incorrecta', 'danger')

    if email_form.validate_on_submit():
        if current_user.check_password_correct(attempted_password=email_form.password.data):
            email_token = gen_confirm_token(email_form.new_email.data)
            user_token = gen_confirm_token(current_user.username)
            send_confirmation_email(
                url_endpoint = url_for('settings.change_email_address', m = email_token, u = user_token, _external = True),
                html_to_send = 'verification/change_email.html',
                email_subject = '[To Do List] Cambio de dirección de correo'
            )
            current_user.active_token = email_token
            db.session.commit()
            return redirect(url_for('settings.main', openModal='mail_change'))
        else:
            flash('La contraseña que ingresó es incorrecta', 'danger')

    return render_template('settings.html', password_form=password_form, email_form=email_form, open_modal=request.args.get('openModal'))

@settings.route('confirm/change-password')
def change_password():
    try:
        new_password = confirm_token(request.args.get('token'))
        username = confirm_token(request.args.get('u'))
    except:
        flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
        return redirect(url_for('routes.home'))

    user = User.query.filter_by(username = username).first_or_404()

    if user:
        if request.args.get('token') != user.active_token:
            flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
            return redirect(url_for('routes.home'))
        user.password = new_password
        user.active_token = ""
        db.session.commit()
        return render_template('change_password.html', password=new_password)
    
    flash('El usuario al que se intenta acceder no existe.', 'warning')
    return redirect(url_for('routes.home'))

@settings.route('confirm/change-address')
def change_email_address():
    try:
        new_email = confirm_token(request.args.get('m'))
        username = confirm_token(request.args.get('u'))
    except:
        flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
        return redirect(url_for('routes.home'))

    user = User.query.filter_by(username = username).first_or_404()

    if user:
        if request.args.get('m') != user.active_token:
            flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
            return redirect(url_for('routes.home'))
        user.email = new_email
        user.active_token = ""
        db.session.commit()
        return render_template('change_email.html', email=new_email)
    
    flash('El usuario al que se intenta acceder no existe.', 'warning')
    return redirect(url_for('routes.home'))

@settings.route('forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email_token = gen_confirm_token(form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        if send_confirmation_email_anon(
            url_endpoint = url_for('settings.reset_password', m = email_token, _external = True),
            html_to_send = 'verification/reset_password.html',
            email_subject = '[To Do List] Reinicio de contraseña',
            email_address = form.email.data,
            url_fallback = url_for('settings.forgot_password')
        ) is True:
            user.active_token = email_token
            db.session.commit()
            flash('Chequee su correo electrónico para completar el proceso', 'info')
            return redirect(url_for('routes.home'))
    return render_template('forgot_password.html', form=form)

@settings.route('reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()

    try:
        email = confirm_token(request.args.get('m'))
    except:
        flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
        return redirect(url_for('routes.home'))

    user = User.query.filter_by(email=email).first_or_404()

    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for('auth.login'))

    if user:
        if request.args.get('m') != user.active_token:
            flash('El link de confirmación es invalido o expiró. Intente nuevamente.', 'danger')
            return redirect(url_for('routes.home'))
        user.active_token = ""
        db.session.commit()
        return render_template('reset_password.html', form=form)
    
    flash('El usuario al que se intenta acceder no existe.', 'warning')
    return redirect(url_for('routes.home'))
