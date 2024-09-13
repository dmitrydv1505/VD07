# Импортируем FlaskForm из flask_wtf для создания форм.
from flask_wtf import FlaskForm
# Импортируем поля для форм из wtforms.
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# Импортируем валидаторы для проверки данных.
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# Импортируем модель User из нашего приложения для проверки уникальности данных.
from app.models import User

# Создаем класс для формы регистрации.
class RegistrationForm(FlaskForm):
    # Поле для ввода имени пользователя с обязательным заполнением и ограничением длины.
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    # Поле для ввода email с обязательным заполнением и проверкой формата email.
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода пароля с обязательным заполнением.
    password = PasswordField('Password', validators=[DataRequired()])
    # Поле для подтверждения пароля с обязательным заполнением и проверкой на совпадение с полем пароля.
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Кнопка отправки формы
    submit = SubmitField('Sign Up')

    # Метод для проверки уникальности имени пользователя.
    def validate_username(self, username):
        # Проверяем, есть ли пользователь с таким именем.
        user = User.query.filter_by(username=username.data).first()
        if user:
            # Если пользователь существует, вызываем ошибку.
            raise ValidationError('Такое имя уже существует')

    # Метод для проверки уникальности email.
    def validate_email(self, email):
        # Проверяем, есть ли пользователь с таким email.
        email = User.query.filter_by(email=email.data).first()
        if email:
            # Если email существует, вызываем ошибку
            raise ValidationError('Такая почта уже используется')


# Создаем класс для формы входа
class LoginForm(FlaskForm):
    # Поле для ввода email с обязательным заполнением и проверкой формата email.
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода пароля с обязательным заполнением
    password = PasswordField('Password', validators=[DataRequired()])
    # Чекбокс для опции "Запомни меня".
    remember = BooleanField('Запомни меня')
    # Кнопка отправки формы
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')
