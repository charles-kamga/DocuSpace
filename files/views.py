from django.shortcuts import render, redirect
from .models import Folder, Document
from django.core.files.storage import FileSystemStorage

def home(request):
    folders = Folder.objects.all()
    documents = Document.objects.all()
    return render(request, 'files/home.html', {'folders': folders, 'documents': documents})

def upload_document(request):
    if request.method == 'POST' and request.FILES['file']:
        title = request.POST['title']
        folder_id = request.POST.get('folder')
        folder = Folder.objects.get(id=folder_id) if folder_id else None
        uploaded_file = request.FILES['file']
        Document.objects.create(
            title=title,
            file=uploaded_file,
            folder=folder,
            owner=request.user
        )
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        Document.objects.create(title=title, file=filename, folder=folder, owner=request.user)
        return redirect('home')

    folders = Folder.objects.all()
    return render(request, 'files/upload.html', {'folders': folders})

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect

# ----- Register -----
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connecter directement après l'inscription
            messages.success(request, "Inscription réussie !")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'files/register.html', {'form': form})

# ----- Login -----
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'files/login.html', {'form': form})

# ----- Logout -----
def logout_view(request):
    logout(request)
    messages.info(request, "Déconnexion réussie !")
    return redirect('login')

from django.contrib.auth.decorators import login_required
from django import forms
from .models import Folder

# Formulaire simple pour créer un dossier
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

@login_required(login_url='login')
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user  # Associer le dossier à l'utilisateur connecté
            folder.save()
            return redirect('home')
    else:
        form = FolderForm()
    return render(request, 'files/create_folder.html', {'form': form})
