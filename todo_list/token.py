from itsdangerous import URLSafeTimedSerializer
from todo_list import app

def gen_confirm_token(text):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(text, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        text = serializer.loads(
            token,
            salt = app.config['SECURITY_PASSWORD_SALT'],
            max_age = expiration
        )
        return text
    except:
        return False
