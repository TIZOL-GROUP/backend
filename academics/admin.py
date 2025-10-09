from django.contrib import admin
from .models import Grade, Attendance, Timetable

admin.site.register(Attendance)
admin.site.register(Grade)
admin.site.register(Timetable)
