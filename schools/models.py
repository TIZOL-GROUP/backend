from django.db import models
from django.conf import settings
# Retrait de PermissionsMixin, qui est inclus dans AbstractUser
from django.contrib.auth.models import AbstractUser, Group 
from django.contrib.auth.hashers import make_password 
import uuid 

class SchoolUser(AbstractUser):
    # CORRECTION : Ajout de related_name pour éviter le conflit avec un autre modèle AbstractUser
    groups = models.ManyToManyField(
        Group,
        related_name='school_user_groups',  # RELATED_NAME UNIQUE
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name="school_user",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='school_user_permissions',  # RELATED_NAME UNIQUE
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name="school_user_permission",
    )

    # La méthode save() problématique a été retirée. 
    # La logique de mot de passe est maintenant dans SchoolUserAdmin.
    pass 

# -----------------------------------------------------------------------

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    # Le superuser qui a créé l'école
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_schools')

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    # L'éducateur qui supervise la classe
    # Utilisation de settings.AUTH_USER_MODEL qui pointe vers SchoolUser ou User
    educator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_classes')

    def __str__(self):
        return f"{self.name} - {self.school.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    # Un enseignant peut enseigner une matière dans plusieurs classes
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subjects_taught')
    # Une matière peut être enseignée dans plusieurs classes
    classes = models.ManyToManyField(Class, related_name='subjects')

    def __str__(self):
        return self.name