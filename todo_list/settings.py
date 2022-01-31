from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from todo_list import db
from todo_list.token import gen_confirm_token, confirm_token
from todo_list.email import send_email
from todo_list.forms import ChangePasswordForm, ChangeEmailForm
from todo_list.models import User

settings = Blueprint('settings', __name__)

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
        user.password = new_password
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
        user.email = new_email
        db.session.commit()
        return render_template('change_email.html', email=new_email)
    
    flash('El usuario al que se intenta acceder no existe.', 'warning')
    return redirect(url_for('routes.home'))
