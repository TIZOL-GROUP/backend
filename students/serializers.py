from rest_framework import serializers
from .models import Student
from users.serializers import UserSerializer
from schools.serializers import ClassSerializer

class StudentSerializer(serializers.ModelSerializer):
    parents = UserSerializer(many=True, read_only=True)
    current_class = ClassSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'current_class', 'parents', 'photo']
