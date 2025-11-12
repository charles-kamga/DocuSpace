import os
from django.core.management.base import BaseCommand
from files.models import Document
from django.db.models import Count

class Command(BaseCommand):
    help = 'Nettoyer les documents en double en conservant la version la plus récente'

    def handle(self, *args, **options):
        # Trouver les titres qui apparaissent plus d'une fois
        duplicates = (
            Document.objects.values('title')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        if not duplicates:
            self.stdout.write(self.style.SUCCESS('Aucun doublon trouvé.'))
            return

        self.stdout.write(f"Traitement de {len(duplicates)} documents en double...")

        for dup in duplicates:
            title = dup['title']
            self.stdout.write(f"\nTraitement des doublons pour: {title}")
            
            # Récupérer tous les documents avec ce titre, triés par date (du plus récent au plus ancien)
            docs = Document.objects.filter(title=title).order_by('-uploaded_at')
            
            # Le premier document est le plus récent, on le conserve
            keeper = docs.first()
            self.stdout.write(f"  - Conservation du document le plus récent: {keeper.file.name} (uploadé le {keeper.uploaded_at})")
            
            # Supprimer les doublons (tous sauf le plus récent)
            for doc in docs[1:]:
                file_path = doc.file.path
                self.stdout.write(f"  - Suppression du doublon: {doc.file.name}")
                
                # Supprimer le fichier physique s'il existe
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        self.stdout.write(f"    - Fichier supprimé: {file_path}")
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"    - Erreur lors de la suppression du fichier {file_path}: {e}"))
                
                # Supprimer l'entrée de la base de données
                doc.delete()
        
        self.stdout.write(self.style.SUCCESS('\nNettoyage des doublons terminé avec succès !'))
