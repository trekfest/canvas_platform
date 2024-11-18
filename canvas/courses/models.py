from django.db import models
from accounts.models import CustomUser

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=50)
    description = models.TextField()
    credits = models.IntegerField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
