from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, ClassViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
