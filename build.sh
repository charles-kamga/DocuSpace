#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Récupération des fichiers statiques
python manage.py collectstatic --no-input

# Migration de la base de données
python manage.py migrate        