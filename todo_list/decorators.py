from flask import flash, redirect, url_for
from flask_login import current_user

# Chequear si el usuario está confirmado
def confirm_required(func):
    def wrapped(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Por favor verifique su cuenta', 'danger')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)
    
    return wrapped
