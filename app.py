from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '1234567890'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class AdminUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
def initialize_db():
    with app.app_context():
        db.create_all()
        
initialize_db()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        flash('Admin Login required!', 'danger')
        return redirect(url_for('admin_login'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logon failed. Please check your username and password.', 'danger')      
    return render_template('login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = AdminUser.query.filter_by(username=username).first()
        
        if admin and admin.password == password:
            flash('Admin Login successful!', 'success')
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Admin Login failed. Please check your credentials.', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/create', methods=['GET', 'POST'])
def admin_create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_admin = AdminUser.query.filter_by(username=username).first()
        if existing_admin:
            flash('Admin username already exists. Please choose another username.', 'danger')
        else:
            new_admin = AdminUser(username=username, password=password)
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin account created successfully!', 'success')
            return redirect(url_for('admin_login'))

    return render_template('admin_create.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another username.', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out successfully!', 'success')
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
    