# 📁 DocuSpace

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.26-092E20.svg?logo=django)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-7952B3.svg?logo=bootstrap)](https://getbootstrap.com/)

DocuSpace est une application web de gestion de documents qui permet de stocker, organiser et gérer facilement vos fichiers en ligne avec une interface utilisateur moderne et intuitive.

## ✨ Fonctionnalités

### 📂 Gestion des dossiers
- Création de dossiers personnalisés
- Organisation hiérarchique des documents
- Renommage et suppression sécurisée
- Affichage du contenu des dossiers

### 📄 Gestion des documents
- Upload multiple de fichiers
- Prévisualisation des fichiers
- Téléchargement et ouverture directe
- Déplacement entre les dossiers
- Renommage et suppression sécurisée

### 👤 Gestion des utilisateurs
- Inscription et authentification
- Espace personnel sécurisé
- Séparation des données par utilisateur

## 🚀 Technologies utilisées

### Backend
- Python 3.12+
- Django 4.2.26
- Django Crispy Forms
- Pillow (traitement d'images)

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5.3.2
- jQuery 3.7.1
- Font Awesome 6.4.0

### Base de données
- SQLite (développement)
- Compatible PostgreSQL/MySQL (production)

## 🛠️ Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/charles-kamga/DocuSpace.git
   cd DocuSpace
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - Site web: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 📝 Structure du projet

```
DocuSpace/
├── DocuSpace/           # Configuration du projet Django
├── files/               # Application principale
│   ├── migrations/      # Fichiers de migration
│   ├── static/          # Fichiers statiques (CSS, JS, images)
│   ├── templates/       # Templates HTML
│   ├── admin.py         # Configuration de l'admin
│   ├── apps.py          # Configuration de l'application
│   ├── forms.py         # Formulaires
│   ├── models.py        # Modèles de données
│   ├── urls.py          # Routes de l'application
│   └── views.py         # Vues de l'application
├── media/               # Fichiers uploadés par les utilisateurs
├── .gitignore           # Fichiers à ignorer par Git
└── requirements.txt     # Dépendances Python
```

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Contact

Pour toute question, contactez charleskamgapr@gmail.com ou ouvrez une issue sur GitHub.
