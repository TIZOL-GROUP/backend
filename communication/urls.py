from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)
router.register(r'chat-messages', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
