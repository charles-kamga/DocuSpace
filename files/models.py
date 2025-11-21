from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def document_upload_path(instance, filename):
    # Cette fonction génère un chemin unique pour chaque fichier
    import os
    from django.utils.text import slugify
    from time import time
    
    # Récupère l'extension du fichier
    ext = filename.split('.')[-1]
    # Crée un nom de fichier unique avec un timestamp
    filename = f"{slugify(instance.title)}_{int(time())}.{ext}"
    # Retourne le chemin complet avec le sous-dossier 'documents'
    return os.path.join('documents', filename)

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=document_upload_path)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
