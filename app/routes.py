# В этом файле пропишем все декораторы для маршрутов, необходимых на сайте. Начнем с импорта нужных библиотек и модулей.
# Импортируем функции Flask для рендеринга HTML-шаблонов, обработки запросов, перенаправления, создания URL и отображения сообщений
from flask import render_template, request, redirect, url_for, flash
# Импортируем функции Flask-Login для управления сессиями пользователей: вход, выход, текущий пользователь и защита маршрутов
from flask_login import login_user, logout_user, current_user, login_required
# Импортируем модель User из приложения для работы с пользователями в базе данных
from app.models import User
# Импортируем экземпляр приложения Flask, базу данных и инструмент для хэширования паролей
from app import app, db, bcrypt
# Импортируем формы регистрации и входа из приложения
from app.forms import RegistrationForm, LoginForm, EditProfileForm

@app.route('/')
@app.route('/home')
# Определяем маршрут для главной страницы сайт
def home():
    # Возвращаем HTML-шаблон home.html для отображения пользователю
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
# Определяем маршрут для страницы регистрации с поддержкой GET и POST запросов
def register():
    # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Создаем экземпляр формы регистрации
    form = RegistrationForm()
    # Проверяем, прошла ли форма валидацию при отправке
    if form.validate_on_submit():
        # Хэшируем пароль пользователя
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Создаем нового пользователя с данными из формы
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Добавляем нового пользователя в сессию базы данных
        db.session.add(user)
        # Сохраняем изменения в базе данных
        db.session.commit()
        # Отправляем пользователю сообщение об успешной регистрации
        flash('Вы успешно зарегистрировались!', 'success')
        # Перенаправляем пользователя на страницу входа
        return redirect(url_for('login'))
    # Если форма не отправлена или не прошла валидацию, отображаем страницу регистрации
    return render_template('register.html', form=form, title='Register')

# Определяем маршрут для страницы входа с поддержкой GET и POST запросов
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Создаем экземпляр формы входа
    form = LoginForm()
    # Проверяем, прошла ли форма валидацию при отправке
    if form.validate_on_submit():
        # Ищем пользователя в базе данных по введенному email
        user = User.query.filter_by(email=form.email.data).first()
        # Проверяем, существует ли пользователь и совпадает ли введенный пароль с хранящимся в базе
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Выполняем вход пользователя в систему и запоминаем его, если установлена соответствующая галочка
            login_user(user, remember=form.remember.data)
            # Перенаправляем пользователя на главную страницу после успешного входа
            return redirect(url_for('home'))
        else:
            # Отправляем пользователю сообщение об ошибке, если данные неверны
            flash('Введены неверные данные')
    # Если форма не отправлена или не прошла валидацию, отображаем страницу входа
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
# Определяем маршрут для выхода из системы
def logout():
    # Выполняем выход пользователя из системы
    logout_user()
    # Перенаправляем пользователя на главную страницу после выхода
    return redirect(url_for('home'))

@app.route('/account')
@login_required
# Определяем маршрут для страницы аккаунта пользователя, доступный только аутентифицированным пользователям
def account():
    # Возвращаем HTML-шаблон account.html для отображения пользователю
    return render_template('account.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Здесь ваш код для обновления профиля пользователя в базе данных
        return redirect(url_for('home'))   # Перенаправляем пользователя на домашнюю страницу

    return render_template('edit_profile.html', title='Редактирование профиля', form=form)