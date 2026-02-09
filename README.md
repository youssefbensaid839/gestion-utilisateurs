# gestion-utilisateurs
# Projet PFE - Application de Gestion d'Utilisateurs

Application web Flask avec :
- Inscription / Connexion sécurisée (mots de passe hachés)
- CRUD simple sur les utilisateurs
- Base de données SQL Server (LocalDB)
- Interface moderne avec Tailwind CSS

## Comment tester localement

1. Installer Python 3.13+
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer : `venv\Scripts\activate`
4. Installer les dépendances : `pip install -r requirements.txt`
5. Configurer la connexion SQL dans `app.py` (URI vers LocalDB)
6. Lancer : `python app.py`
7. Ouvrir : http://127.0.0.1:5000

## Technologies utilisées
- Flask
- Flask-SQLAlchemy
- pyodbc + SQL Server LocalDB
- Tailwind CSS (via CDN)
## Files
- app.py
templates/ (avec login.html, signup.html, crud.html)
static/css/ (avec tailwind.css )
requirements.txt
- Werkzeug pour le hachage des mots de passe

Contact : [ton email ou ton nom]
