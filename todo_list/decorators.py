from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

# Chequear si el usuario está confirmado
def confirm_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.email_confirmed:
            flash('Debe verificar su cuenta para acceder a esa funcionalidad.', 'danger')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)
    
    return wrapped
