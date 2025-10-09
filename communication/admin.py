from django.contrib import admin
from .models import Announcement, ChatMessage 

# Enregistrer le modèle auprès de l'interface d'administration
admin.site.register(Announcement)
admin.site.register(ChatMessage)
# Register your models here.
