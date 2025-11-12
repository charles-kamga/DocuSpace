from django.urls import path
from . import views

urlpatterns = [
    # URLs principales
    path('', views.home, name='home'),
    
    # Gestion des documents
    path('upload/', views.upload_document, name='upload_document'),
    path('delete-document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('rename-document/<int:document_id>/', views.rename_document, name='rename_document'),
    
    # Gestion des dossiers
    path('folder/<int:folder_id>/', views.view_folder, name='view_folder'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('rename-folder/<int:folder_id>/', views.rename_folder, name='rename_folder'),
    path('move-document/<int:document_id>/', views.move_document, name='move_document'),
    
    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
