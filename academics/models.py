from django.db import models
from students.models import Student
from schools.models import Subject, Class
from django.conf import settings

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    score = models.FloatField()
    date = models.DateField()
    assessment_type = models.CharField(max_length=100) # Ex: "Contrôle continu", "Devoir", "Composition"
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='grades_given')

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"

class Timetable(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'MONDAY', 'Lundi'
        TUESDAY = 'TUESDAY', 'Mardi'
        WEDNESDAY = 'WEDNESDAY', 'Mercredi'
        THURSDAY = 'THURSDAY', 'Jeudi'
        FRIDAY = 'FRIDAY', 'Vendredi'
        SATURDAY = 'SATURDAY', 'Samedi'
        SUNDAY = 'SUNDAY', 'Dimanche'

    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetable')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_instance} - {self.subject} on {self.day_of_week}"

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Présent'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'En retard'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)
    reason = models.TextField(blank=True, null=True) # Pour justifier une absence
    # La session de cours concernée (optionnel, mais utile)
    timetable_session = models.ForeignKey(Timetable, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.date}: {self.status}"
