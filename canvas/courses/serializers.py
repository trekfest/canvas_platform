from rest_framework import serializers
from accounts.models import CustomUser
from .models import Course, Enrollment

class CourseEnrollSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    enrollment_date = serializers.DateField(required=False)

    def validate_id(self, value):
        # Ensure the user with the given ID exists and is a student
        try:
            user = CustomUser.objects.get(pk=value, role='student')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("A valid student with this ID does not exist.")
        return value

class CourseNameSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name')  
    
    class Meta:
        model = Enrollment
        fields = ['course_name']

class CourseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']