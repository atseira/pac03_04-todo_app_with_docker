from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import distinct

from . import db
from .models import Todo, User
from .forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/')
@login_required
def index():
    project_name = request.args.get('project_name', '')
    if project_name:
        todo_list = Todo.query.filter_by(user_id=current_user.id, project_name=project_name).all()
    else:
        todo_list = Todo.query.filter_by(user_id=current_user.id).all()

    # Query distinct project names
    projects = db.session.query(distinct(Todo.project_name)).filter_by(user_id=current_user.id).all()

    completed_todos = [todo for todo in todo_list if todo.complete]
    incomplete_todos = [todo for todo in todo_list if not todo.complete]
    return render_template('index.html', completed_todos=completed_todos, incomplete_todos=incomplete_todos, project_name=project_name, projects=projects)

@main.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    project_name = request.form.get('project_name')
    description = request.form.get('description')
    new_todo = Todo(title=title, project_name=project_name, description=description, complete=False, user=current_user)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first() # Ensure the todo belongs to the current user
    if todo:
        todo.title = new_title
        todo.description = new_description
        db.session.commit()
    return redirect(url_for('main.index'))
    
@main.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first() # Ensure the todo belongs to the current user
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first() # Ensure the todo belongs to the current user
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
