from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import CourseEnrollSerializer, CourseNameSerializer, CourseTeacherSerializer
from .models import Course, Enrollment
from accounts.models import CustomUser
from rest_framework import generics
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow access to admins (superusers).
    """
    def has_permission(self, request, view):
        return request.user.is_superuser
    
class IsTeacher(BasePermission):
    """
    Custom permission to only allow access to teachers.
    """
    def has_permission(self, request, view):
        return request.user.role == 'teacher'
    
class IsStudent(BasePermission):
    """
    Custom permission to only allow access to teachers.
    """
    def has_permission(self, request, view):
        return request.user.role == 'student'
    

class CourseEnrollView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Decode the token and check if the user is an admin
        user = request.user

        if user.role != 'admin':
            return Response({"error": "You do not have permission to perform this action. Admin access required."}, status=status.HTTP_403_FORBIDDEN)

        # Get the course
        course = get_object_or_404(Course, pk=pk)

        # Validate the request data using the serializer
        serializer = CourseEnrollSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        student_id = serializer.validated_data['id']
        enrollment_date = request.data.get('enrollment_date', now())

        # Ensure the student exists and isn't already enrolled
        student = CustomUser.objects.get(pk=student_id)
        if Enrollment.objects.filter(course=course, student=student).exists():
            return Response({"error": "Student is already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

        # Enroll the student
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            enrollment_date=enrollment_date
        )

        return Response(
            {
                "message": "Student enrolled successfully.",
                "enrollment": {
                    "id": enrollment.id,
                    "student": {
                        "id": student.id,
                        "email": student.email,
                        "name": f"{student.first_name} {student.last_name}"
                    },
                    "course": {
                        "id": course.id,
                        "name": course.course_name
                    },
                    "enrollment_date": enrollment.enrollment_date,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class CourseEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            # Retrieve the course by its ID
            course = Course.objects.get(id=course_id)

            # Get all enrollments for the course
            enrollments = Enrollment.objects.filter(course=course)

            if not enrollments.exists():
                return Response({"message": "No students enrolled in this course."}, status=status.HTTP_404_NOT_FOUND)

            # Prepare the student data
            students_data = []
            for enrollment in enrollments:
                student_data = {
                    "id": enrollment.student.id,
                    "full name": f"{enrollment.student.first_name} {enrollment.student.last_name}", 
                    "email": enrollment.student.email,
                    "enrollment_date": enrollment.enrollment_date,
                }
                students_data.append(student_data)

            # Return the course and its enrolled students
            course_data = {
                "course": {
                    "id": course.id,
                    "name": course.course_name,
                    "code": course.course_code
                },
                "students": students_data
            }

            return Response(course_data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

class TeacherAssignedCoursesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]  
    serializer_class = CourseTeacherSerializer

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(teacher=user)
    
class StudentEnrolledCoursesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]  
    serializer_class = CourseNameSerializer

    def get_queryset(self):
        user = self.request.user
        return Enrollment.objects.filter(student=user).select_related('course')
