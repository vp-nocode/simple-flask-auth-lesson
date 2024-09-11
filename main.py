from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm # Это базовый класс для создания форм
from wtforms import StringField, SubmitField # Это классы для создания полей внутри формы
from wtforms.validators import DataRequired # Валидатор, нуный для проверки

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db' # Эта строчка нужна, чтобы мы могли подключиться к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Эта строчка отключает сигнализацию об изменении объектов внутри базы данных
app.config['SECRET_KEY'] = 'your_secret_key_1001'
db = SQLAlchemy(app) # Создание объекта, через который мы будем работать с базой данных

class NameForm(FlaskForm): # Используем FlaskForm в качестве родительского класса
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class User(db.Model): # В скобках указываем модель, чтобы в дальнейшем создать именно базу данных
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # В скобках описываем поля таблицы

    def __repr__(self): # Этот метод определяет, как объект модели будет выглядеть в виде строки
        return f'[User {self.username}]'

with app.app_context(): # Функция создаёт контекст приложения, который нужен для работы с базой данных
    db.create_all() # Создание всей таблицы, которые определены в классе User

@app.route('/add_user/<name>') # С помощью декоратора создаём маршрут, который будет вызывать функцию
def add_user(name): # Функция будет создавать объект класса User
    # new_user = User(username='new_username_1')
    new_user = User(username=name)
    db.session.add(new_user) # Добавляем в сессию
    db.session.commit() #  Сохраняем изменения в базу данных
    return 'User added' # Вывод сообщения о том, что юзер добавлен в базу данных

@app.route('/users')
def get_users():
    users = User.query.all() # Получаем всех юзеров из базы данных и сохраняем в переменную users
    return str(users)

@app.route('/', methods=['GET', 'POST']) #  С помощью этого маршрута мы сможем и отправлять, и получать информацию
def index():
    form = NameForm() #  Создаём объект формы
    if form.validate_on_submit(): # Проверка того, прошла ли форма валидацию и вообще отправлена ли она
        name = form.name.data #  Получаем значение из формы, информацию из этого значения. Сохраняем в переменную
        return redirect(url_for('hello', name=name)) # Отправляем пользователя на новую страницу, передаём полученное имя
    return render_template('index.html', form=form)

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'


if __name__ == '__main__':
    app.run(debug=True)