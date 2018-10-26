from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.debug = True

app.config['MYSQL_HOST'] = 'database.mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask_blog'
app.config['MYSQL_CURSORCALSS'] = 'DictCursor'

mysql = MySQL(app)

articlesData = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = articlesData)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

class RegisterForm(Form):
    name = StringField('Name', validators=[validators.Length(min=1, max=256), validators.input_required()])
    username  = StringField('Username', validators=[validators.Length(min=4, max=256)])
    email  = StringField('E-mail', validators=[validators.Length(min=6, max=256)])
    password  = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if (request.method == 'POST' and form.validate):
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(`name`, `email`, `username`, `password`) VALUES (%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered can log in', 'success')

        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'AC643BA6F0DEFEC18F96C9DF272E50A9441CC1E5D7D91'
    app.run()
