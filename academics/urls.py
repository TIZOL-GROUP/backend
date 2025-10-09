from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GradeViewSet, TimetableViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'grades', GradeViewSet)
router.register(r'timetables', TimetableViewSet)
router.register(r'attendances', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
