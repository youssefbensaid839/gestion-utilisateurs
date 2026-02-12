# app.py - Flask backend with SQL Server integration

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
import pyodbc  # Required for SQL Server connection, but SQLAlchemy handles it via dialect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 'your_secret_key'  # Change this to a secure random key

# SQL Server connection string
# Replace with your own: SERVER, DATABASE, USER, PASSWORD
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://@'
    '(localdb)\\MSSQLLocalDB'                  # ← double backslash obligatoire ici !
    '/TestCRUD'                     # ← nom de ta base (crée-la si besoin)
    '?driver=ODBC+Driver+18+for+SQL+Server'
    '&Trusted_Connection=yes'
    '&TrustServerCertificate=yes'              # ← ajoute ça !
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create the database tables (run once or use migrations in production)
with app.app_context():
    db.create_all()

# Home route - redirects to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('crud'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('login'))

# CRUD example route (protected - requires login)
# For simplicity, CRUD on users (list, create already in signup, update, delete)
@app.route('/crud', methods=['GET', 'POST'])
def crud():
    if 'user_id' not in session:
        flash('Please log in', 'error')
        return redirect(url_for('login'))
    
    users = User.query.all()  # Read all users
    return render_template('crud.html', users=users)
# Route pour UPDATE (modifier l'email d'un utilisateur)
@app.route('/users/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    if 'user_id' not in session:
        flash('Veuillez vous connecter', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)  # 404 si l'utilisateur n'existe pas
    
    new_email = request.form.get('new_email')
    if not new_email:
        flash('Nouvelle adresse email requise', 'error')
        return redirect(url_for('crud'))
    
    # Optionnel : vérifier que l'email n'est pas déjà pris par un autre
    existing = User.query.filter_by(email=new_email).first()
    if existing and existing.id != user_id:
        flash('Cet email est déjà utilisé', 'error')
        return redirect(url_for('crud'))
    
    user.email = new_email
    db.session.commit()
    flash('Utilisateur mis à jour avec succès', 'success')
    
    return redirect(url_for('crud'))


# Route pour DELETE (supprimer un utilisateur)
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        flash('Veuillez vous connecter', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    # Optionnel : empêcher de supprimer son propre compte
    if user.id == session['user_id']:
        flash('Vous ne pouvez pas supprimer votre propre compte', 'error')
        return redirect(url_for('crud'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès', 'success')
    
    return redirect(url_for('crud'))
if __name__ == '__main__':
    app.run(debug=True)
