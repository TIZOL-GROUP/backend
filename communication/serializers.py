from rest_framework import serializers
from .models import Announcement, ChatMessage
from schools.serializers import SchoolSerializer
from users.serializers import UserSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'school', 'title', 'content', 'created_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp', 'is_read']
