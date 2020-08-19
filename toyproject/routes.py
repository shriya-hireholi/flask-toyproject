from flask import render_template, url_for, redirect, flash, request
from toyproject import db, app, bcrypt
from toyproject.forms import RegistrationForm, LoginForm, NewTaskForm
from toyproject.models import User, Todo
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('You are now Logged in', 'success')
        return redirect(url_for('login_page'))
    return render_template("register.html", title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(
                                    user.password,
                                    form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been Logged In', 'success')
            return redirect(url_for('home_page'))
        else:
            flash(
                'Login Unsuccessful, Please check email and password',
                'danger')

    return render_template("login.html", title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    form = NewTaskForm()
    if form.validate_on_submit():
        new_task = Todo(content=form.content.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home_page'))

    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('home.html', title='Home', form=form, tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('home_page'))
    except Exception:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('home_page'))
        except Exception:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
