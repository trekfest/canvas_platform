from django.urls import path
from .views import CourseEnrollView, CourseEnrollmentsView, StudentEnrolledCoursesView, TeacherAssignedCoursesView

urlpatterns = [
    path('<int:pk>/enroll/', CourseEnrollView.as_view(), name='course-enroll'),
    path('<int:course_id>/enrollments/', CourseEnrollmentsView.as_view(), name='course-enrollments'),
    path('teacher/courses/', TeacherAssignedCoursesView.as_view(), name='teacher-assigned-courses'),
    path('student/courses/', StudentEnrolledCoursesView.as_view(), name='student-enrolled-courses'),
]
