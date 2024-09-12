# Импортируем класс Flask из библиотеки flask для создания веб-приложения.
from flask import Flask

# Импортируем SQLAlchemy для работы с базой данных.
from flask_sqlalchemy import SQLAlchemy

# Импортируем Bcrypt для хеширования паролей.
from flask_bcrypt import Bcrypt

# Импортируем LoginManager для управления сессиями пользователей.
from flask_login import LoginManager

# Создаем экземпляр Flask-приложения с именем текущего модуля.
app = Flask(__name__)

# Устанавливаем секретный ключ для безопасности сессий и токенов.
app.config['SECRET_KEY'] = 'your_secret_key'

# Указываем путь к базе данных SQLite.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Создаем экземпляр SQLAlchemy, связанный с нашим приложением, для работы с БД.
db = SQLAlchemy(app)

# Создаем экземпляр Bcrypt для шифрования паролей в нашем приложении.
bcrypt = Bcrypt(app)

# Создаем экземпляр LoginManager для управления авторизацией пользователей.
login_manager = LoginManager(app)

# Указываем, что при необходимости входа пользователя будет использоваться представление 'login'.
login_manager.login_view = 'login'

# Импортируем модуль routes, который содержит маршруты/путь нашего приложения.
from app import routes