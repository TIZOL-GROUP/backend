from rest_framework import serializers
from .models import School, Class, Subject
from users.serializers import UserSerializer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class ClassSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    educator = UserSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'school', 'educator', 'subjects']

class SchoolSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'created_by', 'classes']
