
# Импортируем необходимые объекты из нашего приложения: базу данных и менеджер входа.
from app import db, login_manager
# # Импортируем UserMixin для упрощения работы с пользователями в Flask-Login.
from flask_login import UserMixin

#  Создаём декоратор, который сообщает Flask, что функция будет использоваться для загрузки пользователя по его ID:
@login_manager.user_loader
def load_user(user_id):
    # Возвращает пользователя из базы данных по его ID.
    return User.query.get(int(user_id))

# Создаём класс User, который будет представлять пользователей в нашей базе данных.
class User(db.Model, UserMixin):
    # Уникальный идентификатор каждого пользователя.
    id = db.Column(db.Integer, primary_key=True)
    # Имя пользователя, максимум 20 символов, уникальное и обязательное
    username = db.Column(db.String(20), unique=True, nullable=False)
    # Email пользователя, максимум 120 символов, уникальный и обязательный.
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Хешированный пароль пользователя, обязательный.
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        # Возвращает строковое представление объекта пользователя.
        return f'User: {self.username}, email: {self.email}'