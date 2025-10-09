from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SCHOOL_ADMIN = 'SCHOOL_ADMIN', 'School Admin'
        TEACHER = 'TEACHER', 'Teacher'
        EDUCATOR = 'EDUCATOR', 'Educator'
        PARENT = 'PARENT', 'Parent'

    role = models.CharField(max_length=50, choices=Role.choices)
    
    # Vous pouvez ajouter d'autres champs communs ici si nécessaire
    # par exemple : phone_number, profile_picture, etc.

    def save(self, *args, **kwargs):
        if not self.pk:
            # This is a new user, we can set a default role or perform other actions
            pass
        super().save(*args, **kwargs)
