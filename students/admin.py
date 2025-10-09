from django.contrib import admin
# Importer le modèle que vous voulez gérer
from .models import Student 

# Enregistrer le modèle auprès de l'interface d'administration
admin.site.register(Student)

# Register your models here.
