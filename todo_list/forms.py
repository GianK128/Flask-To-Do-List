from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from todo_list.models import User, List
from flask_login import current_user

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Ese usuario ya está registrado')
    
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Ese correo ya está siendo utilizado')
    
    username = StringField(label='Nombre de usuario', validators=[Length(2, 30), DataRequired()])
    email = StringField(label='Correo electrónico', validators=[Length(8), Email(), DataRequired()])
    password = PasswordField(label='Contraseña', validators=[Length(8, 60), DataRequired()])
    passwordconfirm = PasswordField(label='Confirmar contraseña', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Crear cuenta')

class LoginForm(FlaskForm):
    username = StringField(label='Nombre de usuario', validators=[Length(2, 30), DataRequired()])
    password = PasswordField(label='Contraseña:', validators=[Length(8, 60), DataRequired()])
    submit = SubmitField(label='Entrar')

class CreateListForm(FlaskForm):
    name = StringField(label='Nombre de la Lista', validators=[Length(2), DataRequired()])
    submit = SubmitField(label='Crear')

class DeleteListForm(FlaskForm):
    def validate_id(self, id_to_check):
        list = List.query.filter_by(id=id_to_check.data).first()
        if list.user_id != current_user.id:
            raise ValidationError("No tienes permiso para realizar esta acción")

    id = StringField(validators=[DataRequired()])
    submit = SubmitField(label='Borrar')

class AddItemForm(FlaskForm):
    def validate_list_id(self, list_id_to_check):
        _list = List.query.filter_by(id=list_id_to_check.data).first()
        if _list.user_id != current_user.id:
            raise ValidationError("No tienes permiso para realizar esta acción")

    content = StringField(label='Contenido del Item', validators=[Length(2, 280), DataRequired()])
    list_id = StringField(validators=[DataRequired()])
    submit = SubmitField(label='Agregar Item')

class EditItemForm(FlaskForm):
    def validate_list_id(self, list_id_to_check):
        _list = List.query.filter_by(id=list_id_to_check.data).first()
        if _list.user_id != current_user.id:
            raise ValidationError("No tienes permiso para realizar esta acción")
    
    id = StringField(validators=[DataRequired()])
    list_id = StringField(validators=[DataRequired()])
    submit = SubmitField()

class ProfilePicForm(FlaskForm):
    def validate_id(self, id_to_check):
        if int(id_to_check.data) != current_user.id:
            raise ValidationError("No tienes permiso para realizar esta acción")

    id = StringField(validators=[DataRequired()])
    image = FileField("Elegir una imagen", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Solo se permiten imagenes (jpg, png).')])
    region = StringField(validators=[DataRequired()])
    submit = SubmitField("Subir imagen")
