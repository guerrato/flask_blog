from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.debug = True

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
        validators.EqualTo('confirm', message='Passwords do not match'),
        validators.Length(min=6, max=256)
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if (request.method == 'POST' and form.validate):
        pass
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run()
