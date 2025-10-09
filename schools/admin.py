from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
import random
import string

from .models import SchoolUser, School, Class, Subject 

# ------------------------------------------------------------------
# 1. SchoolUserAdmin : Pour la création directe d'utilisateurs SchoolUser (ex: superuser)
# ------------------------------------------------------------------
class SchoolUserAdmin(UserAdmin):
    # Surcharge de la méthode de sauvegarde de l'Admin pour générer le mot de passe
    def save_model(self, request, obj, form, change):
        # La génération se produit SEULEMENT lors de la CRÉATION
        if not obj.pk: 
            
            # Logique de génération alphanumérique de 6 caractères
            caracteres = string.ascii_letters + string.digits
            raw_password = ''.join(random.choice(caracteres) for i in range(6))
            
            # Hachage et enregistrement du mot de passe
            obj.password = make_password(raw_password)
            obj._initial_password = raw_password # Mot de passe en clair pour l'affichage/envoi (temporaire)

        super().save_model(request, obj, form, change)


# ------------------------------------------------------------------
# 2. SchoolAdmin : Pour la création d'une École et de son utilisateur associé
# ------------------------------------------------------------------
class SchoolAdmin(admin.ModelAdmin):
    # La méthode save_model crée à la fois l'École (School) et son Utilisateur (SchoolUser)
    def save_model(self, request, obj, form, change):
        # 1. Sauvegarde de l'École pour obtenir son PK/ID
        super().save_model(request, obj, form, change)

        # 2. Logique exécutée SEULEMENT LORS DE LA CRÉATION de l'École
        if not change:
            
            # a. Génération du mot de passe (6 caractères alphanumériques)
            caracteres = string.ascii_letters + string.digits
            raw_password = ''.join(random.choice(caracteres) for i in range(6))

            # b. Création de l'utilisateur SchoolUser
            # Assurez-vous que le nom d'utilisateur est unique
            username_base = f"admin_{obj.name.replace(' ', '_').replace('.', '')[:20]}"
            
            school_user = SchoolUser.objects.create(
                username=username_base,
                is_staff=True, # L'utilisateur école doit pouvoir se connecter à l'admin
                is_active=True,
                # Vous pouvez ajouter l'e-mail ici si vous le collectez dans le formulaire School
            )
            
            # c. Hachage et définition du mot de passe
            school_user.password = make_password(raw_password)
            school_user.save()

            # d. Optionnel : Stocker le mot de passe en clair pour l'utilisateur
            # (Vous devriez l'afficher à l'utilisateur ou l'envoyer par email)
            obj._initial_password = raw_password
            
            # e. Optionnel : Créer un lien entre l'École et l'utilisateur admin créé
            # Si SchoolUser a un champ ForeignKey vers School.

# ------------------------------------------------------------------
# 3. Enregistrement des Modèles
# ------------------------------------------------------------------

admin.site.register(SchoolUser, SchoolUserAdmin)
admin.site.register(School, SchoolAdmin) # Utilisation de la classe personnalisée
admin.site.register(Class)
admin.site.register(Subject)