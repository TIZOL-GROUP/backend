from django.db import models
from django.conf import settings
from schools.models import Class

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    # La classe de l'élève
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    # Un élève peut avoir plusieurs parents (tuteurs)
    parents = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='children')
    # Photo optionnelle
    photo = models.ImageField(upload_to='students_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
