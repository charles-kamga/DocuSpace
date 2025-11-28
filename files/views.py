from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Document, Folder
from django.utils.text import slugify
import os
from django.conf import settings

@login_required(login_url='login')
def home(request):
    """
    Vue sécurisée pour la page d'accueil.
    Affiche uniquement les dossiers et documents de l'utilisateur connecté.
    """
    # Récupère uniquement les dossiers racine (sans parent) appartenant à l'utilisateur connecté
    folders = Folder.objects.filter(owner=request.user, parent__isnull=True)

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
            messages.success(request, f"Bienvenue, {user.username} Dans votre espace Document !")
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
    parent_id = request.GET.get('parent')
    parent_folder = None
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)
    
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.parent = parent_folder
            folder.save()
            messages.success(request, f"Le dossier '{folder.name}' a été créé avec succès !")
            if parent_folder:
                return redirect('view_folder', folder_id=parent_folder.id)
            return redirect('home')
    else:
        form = FolderForm()

    return render(request, 'files/create_folder.html', {
        'form': form,
        'parent_folder': parent_folder
    })


@login_required(login_url='login')
def delete_document(request, doc_id):
    """
    Vue sécurisée pour la suppression d'un document.
    Seul le propriétaire du document peut le supprimer.
    """
    # Récupérer le document seulement s'il appartient à l'utilisateur connecté
    doc = Document.objects.filter(owner=request.user, id=doc_id).first()
    
    # Vérifier si le document existe et appartient à l'utilisateur
    if not doc:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce document.")
    
    # Supprimer le document
    doc.delete()
    messages.success(request, "Le document a été supprimé avec succès.")
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='login')
def delete_folder(request, folder_id):
    """
    Vue sécurisée pour la suppression d'un dossier et de son contenu.
    Seul le propriétaire du dossier peut le supprimer.
    """
    # Récupérer le dossier seulement s'il appartient à l'utilisateur connecté
    folder = Folder.objects.filter(owner=request.user, id=folder_id).first()
    
    # Vérifier si le dossier existe et appartient à l'utilisateur
    if not folder:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce dossier.")
    
    # Supprimer tous les documents du dossier puis le dossier lui-même
    folder_name = folder.name
    folder.documents.all().delete()
    folder.delete()
    
    messages.success(request, f"Le dossier '{folder_name}' et son contenu ont été supprimés avec succès.")
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='login')
def rename_document(request, document_id):
    """
    Vue pour renommer un document.
    Seul le propriétaire du document peut le renommer.
    """
    # Récupère le document uniquement s'il appartient à l'utilisateur connecté
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title and new_title.strip():
            document.title = new_title.strip()
            document.save()
            messages.success(request, "Le document a été renommé avec succès.")
            return redirect('home')
        else:
            messages.error(request, "Le titre ne peut pas être vide.")
    
    return render(request, 'files/rename_document.html', {'document': document})


@login_required(login_url='login')
def rename_folder(request, folder_id):
    """
    Vue pour renommer un dossier.
    Seul le propriétaire du dossier peut le renommer.
    """
    # Récupère le dossier uniquement s'il appartient à l'utilisateur connecté
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name and new_name.strip():
            folder.name = new_name.strip()
            folder.save()
            messages.success(request, "Le dossier a été renommé avec succès.")
            return redirect('home')
        else:
            messages.error(request, "Le nom ne peut pas être vide.")
    
    return render(request, 'files/rename_folder.html', {'folder': folder})


@login_required(login_url='login')
def view_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)

    if folder.owner != request.user:
        return HttpResponseForbidden("Interdit.")

    # Récupère les documents et les sous-dossiers
    documents = Document.objects.filter(folder=folder, owner=request.user)
    subfolders = Folder.objects.filter(parent=folder, owner=request.user)

    return render(request, 'files/folder_detail.html', {
        'folder': folder,
        'documents': documents,
        'subfolders': subfolders
    })


@login_required(login_url='login')
def move_document(request, document_id):
    """
    Vue pour déplacer un document d'un dossier à un autre.
    Seul le propriétaire du document peut le déplacer.
    """
    document = get_object_or_404(Document, id=document_id)
    
    # Vérifier que l'utilisateur est le propriétaire du document
    if document.owner != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette ressource.")
    
    if request.method == 'POST':
        folder_id = request.POST.get('folder')
        
        # Si l'utilisateur a sélectionné 'Aucun dossier' (valeur vide)
        if folder_id == '':
            document.folder = None
            document.save()
            messages.success(request, f'Le document a été déplacé vers la racine avec succès.')
            return redirect('home')
        
        # Vérifier que le dossier de destination appartient bien à l'utilisateur
        try:
            folder = Folder.objects.get(id=folder_id, owner=request.user)
            document.folder = folder
            document.save()
            
            messages.success(
                request, 
                f"Le document « {document.title} » a été déplacé vers le dossier « {folder.name} »."
            )
            return redirect('home')
            
        except Exception as e:
            # En cas d'erreur inattendue
            messages.error(
                request, 
                f"Une erreur s'est produite lors du déplacement du document : {str(e)}"
            )
            return redirect('home')

    # GET : Affiche le formulaire de déplacement
    # Définition du dossier courant du document
    current_folder = document.folder
    folders = Folder.objects.filter(owner=request.user).exclude(id=document.folder.id if document.folder else None)
    
    return render(request, 'files/move_document.html', {
        'document': document,
        'folders': folders,
        'current_folder': current_folder
    })
