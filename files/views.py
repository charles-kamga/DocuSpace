from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Folder, Document

@login_required(login_url='login')
def home(request):
    """
    Vue sécurisée pour la page d'accueil.
    Affiche uniquement les dossiers et documents de l'utilisateur connecté.
    """
    # Récupère uniquement les dossiers appartenant à l'utilisateur connecté
    folders = Folder.objects.filter(owner=request.user)

    # Récupère uniquement les documents sans dossier appartenant à l'utilisateur connecté
    documents_without_folder = Document.objects.filter(owner=request.user, folder__isnull=True)

    return render(request, 'files/home.html', {
        'folders': folders,
        'documents_without_folder': documents_without_folder
    })

@login_required(login_url='login')
def upload_document(request):
    """
    Vue sécurisée pour l'upload de documents.
    Vérifie que l'utilisateur ne peut uploader que dans ses propres dossiers.
    """
    if request.method == 'POST' and request.FILES.get('file'):
        title = request.POST['title']
        folder_id = request.POST.get('folder')
        
        # Vérification de sécurité : s'assurer que le dossier appartient bien à l'utilisateur
        folder = Folder.objects.filter(owner=request.user, id=folder_id).first() if folder_id else None
        uploaded_file = request.FILES['file']

        # Nettoyer le nom du fichier (remplacer les espaces par _)
        uploaded_file.name = uploaded_file.name.replace(" ", "_")

        # Créer le document en s'assurant qu'il appartient à l'utilisateur
        Document.objects.create(
            title=title,
            file=uploaded_file,
            folder=folder,
            owner=request.user  # L'utilisateur connecté est toujours le propriétaire
        )

        messages.success(request, "Document téléversé avec succès !")
        return redirect('home')

    # Afficher uniquement les dossiers de l'utilisateur connecté
    folders = Folder.objects.filter(owner=request.user)
    return render(request, 'files/upload.html', {'folders': folders})



def register_view(request):
    """
    Vue d'inscription des utilisateurs.
    Redirige vers la page d'accueil après une inscription réussie.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            messages.success(request, "Inscription réussie ! Vous êtes maintenant connecté.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'files/register.html', {'form': form})

def login_view(request):
    """
    Vue de connexion des utilisateurs.
    Affiche un message de bienvenue après connexion.
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} !")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'files/login.html', {'form': form})

def logout_view(request):
    """
    Vue de déconnexion.
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

# Formulaire pour la création de dossiers avec validation
class FolderForm(forms.ModelForm):
    """
    Formulaire pour la création de dossiers.
    Valide que le nom du dossier n'est pas vide.
    """
    class Meta:
        model = Folder
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du dossier'})
        }

@login_required(login_url='login')
def create_folder(request):
    """
    Vue sécurisée pour la création de dossiers.
    Chaque dossier créé est automatiquement associé à l'utilisateur connecté.
    """
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            # Création du dossier avec l'utilisateur connecté comme propriétaire
            folder = form.save(commit=False)
            folder.owner = request.user  # Sécurité : association automatique à l'utilisateur connecté
            folder.save()
            messages.success(request, f"Le dossier '{folder.name}' a été créé avec succès !")
            return redirect('home')
    else:
        form = FolderForm()
    
    return render(request, 'files/create_folder.html', {'form': form})
