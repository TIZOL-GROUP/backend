from rest_framework import serializers
from .models import Grade, Timetable, Attendance
from students.serializers import StudentSerializer
from schools.serializers import SubjectSerializer, ClassSerializer
from users.serializers import UserSerializer

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'score', 'date', 'assessment_type', 'teacher']

class TimetableSerializer(serializers.ModelSerializer):
    class_instance = ClassSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Timetable
        fields = ['id', 'class_instance', 'subject', 'day_of_week', 'start_time', 'end_time']

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    timetable_session = TimetableSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status', 'reason', 'timetable_session']
